from __future__ import annotations

import time
from typing import List

from controller.config import DetectionContext, DetectionResult
from detectors.base import AnomalyModel, SklearnAnomalyModel
from events.base import Event, LoginEvent, NetworkEvent, SystemEvent


class MLAnomalyDetector:
    """
    ML-based anomaly detector using scikit-learn Isolation Forest.

    Continuously learns from event patterns and detects anomalous behavior
    that deviates from normal baselines. Features include timing patterns,
    success rates, and traffic volumes.
    """

    def __init__(self, model: AnomalyModel | None = None, threshold: float = 0.7) -> None:
        self.name = "MLAnomalyDetector"
        self.model = model or SklearnAnomalyModel(contamination=0.15)
        self.threshold = max(0.0, min(1.0, threshold))
        self.training_features: List[List[float]] = []
        self.last_training_time = 0.0
        self.training_interval = 300  # Retrain every 5 minutes
        self.max_training_samples = 1000

    def _extract_features(self, event: Event) -> List[float]:
        """Extract comprehensive features for anomaly detection."""
        current_time = time.time()
        hour_of_day = (current_time % 86400) / 3600  # 0-24 hour
        day_of_week = ((current_time // 86400) % 7) / 7  # 0-1 normalized

        if isinstance(event, LoginEvent):
            # Login event features
            return [
                1.0,  # event type: login
                1.0 if event.success else 0.0,  # success flag
                len(event.username) / 50.0,  # username length (normalized)
                hash(event.ip_address) % 1000 / 1000.0,  # IP hash (normalized)
                hour_of_day / 24.0,  # time of day
                day_of_week,  # day of week
            ]
        elif isinstance(event, NetworkEvent):
            # Network event features
            max_bytes = 1e6  # 1MB normalization factor
            return [
                2.0,  # event type: network
                # normalized bytes sent
                min(event.bytes_sent / max_bytes, 1.0),
                # normalized bytes received
                min(event.bytes_received / max_bytes, 1.0),
                hash(event.src_ip) % 1000 / 1000.0,  # source IP hash
                hash(event.dst_ip) % 1000 / 1000.0,  # dest IP hash
                hour_of_day / 24.0,  # time of day
            ]
        elif isinstance(event, SystemEvent):
            # System event features
            return [
                3.0,  # event type: system
                hash(event.event_type) % 100 / 100.0,  # event type hash
                len(str(event.details)) / 1000.0,  # details size
                hour_of_day / 24.0,  # time of day
                day_of_week,  # day of week
                0.0,  # padding
            ]
        else:
            # Unknown event type
            return [0.0, 0.0, 0.0, 0.0, hour_of_day / 24.0, day_of_week]

    def _maybe_retrain(self) -> None:
        """Retrain model periodically with accumulated features."""
        current_time = time.time()
        if (current_time - self.last_training_time > self.training_interval
                and len(self.training_features) > 20):

            # Use recent samples for training
            recent_features = self.training_features[-self.max_training_samples:]
            self.model.fit(recent_features)
            self.last_training_time = current_time

    def analyze(self, event: Event, ctx: DetectionContext) -> List[DetectionResult]:
        """Analyze event for anomalies using ML model."""
        features = self._extract_features(event)

        # Add to training data for continuous learning
        self.training_features.append(features)
        if len(self.training_features) > self.max_training_samples:
            self.training_features.pop(0)

        # Periodically retrain model
        self._maybe_retrain()

        # Score the current event
        anomaly_score = self.model.score(features)

        if anomaly_score >= self.threshold:
            # Calculate severity based on how anomalous it is
            severity = min(10, max(1, int(5 + (anomaly_score * 5))))

            desc = (
                f"ML anomaly detected (score={anomaly_score:.3f} >= {self.threshold:.3f}). "
                f"Event pattern deviates significantly from learned baseline."
            )

            return [
                DetectionResult(
                    severity=severity,
                    description=desc,
                    source_detector=self.name,
                )
            ]

        return []
