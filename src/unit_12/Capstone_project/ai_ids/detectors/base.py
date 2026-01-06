from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

from controller.config import DetectionContext, DetectionResult
from events.base import Event

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AnomalyModel(Protocol):
    """Protocol defining the interface for anomaly detection models.

    Defines the contract for machine learning models used in anomaly detection,
    supporting both training (fit) and inference (score) operations.
    """

    def fit(self, features: List[List[float]]) -> None: ...
    def score(self, sample: List[float]) -> float: ...


class DummyAnomalyModel:
    """Placeholder anomaly model for structure; can be swapped with a real ML model."""

    def fit(self, features: List[List[float]]) -> None:
        # No-op
        return None

    def score(self, sample: List[float]) -> float:
        # Always non-anomalous
        return 0.0


class SklearnAnomalyModel:
    """Real scikit-learn based anomaly detection using Isolation Forest.

    Isolation Forest is particularly well-suited for anomaly detection in
    security contexts as it efficiently identifies outliers in multivariate data.
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42) -> None:
        if not SKLEARN_AVAILABLE:
            raise ImportError(
                "scikit-learn is required for SklearnAnomalyModel")

        self.model = IsolationForest(
            contamination=contamination,  # Expected proportion of anomalies
            random_state=random_state,
            n_estimators=100,
        )
        self.is_fitted = False
        self.min_samples_to_fit = 20  # Minimum samples needed for reliable training

    def fit(self, features: List[List[float]]) -> None:
        """Train the isolation forest on historical data."""
        if len(features) >= self.min_samples_to_fit:
            self.model.fit(features)
            self.is_fitted = True

    def score(self, sample: List[float]) -> float:
        """Score a sample for anomaly (0.0 = normal, 1.0 = anomaly)."""
        if not self.is_fitted:
            return 0.0  # No anomaly if model not trained

        try:
            # Isolation Forest returns -1 for anomalies, 1 for normal
            prediction = self.model.predict([sample])
            anomaly_score = self.model.decision_function([sample])[0]

            # Convert to 0-1 scale: more negative = more anomalous
            # Normalize the score to [0, 1] range
            normalized_score = max(0.0, min(1.0, (-anomaly_score + 0.5) / 1.0))

            return normalized_score if prediction[0] == -1 else 0.0
        except Exception:
            return 0.0  # Return safe default on any error


class Detector(ABC):
    """Abstract base class for all intrusion detection mechanisms.

    Defines the common interface for analyzing events and producing
    detection results. All detector implementations must inherit from this class.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def analyze(self, event: Event, ctx: DetectionContext) -> List[DetectionResult]:
        ...


class Rule(ABC):
    """Abstract base class for rule-based detection logic.

    Represents a single detection rule that can evaluate events and
    return a detection result if the rule conditions are met.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def match(self, event: Event, ctx: DetectionContext) -> Optional[DetectionResult]:
        ...

    @abstractmethod
    def describe(self) -> str:
        ...
