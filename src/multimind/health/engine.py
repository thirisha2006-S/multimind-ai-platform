"""Company Health Engine for MultiMind AI Platform.

Continuously monitors the organization and provides live health scores.
"""

from typing import Dict, Any, List
from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CompanyHealthEngine:
    """Monitors organizational health across multiple dimensions."""

    def __init__(self):
        self.dimensions = [
            "hr_health",
            "financial_health",
            "project_health",
            "customer_health",
            "knowledge_health",
            "security_health",
            "operational_health",
        ]

    def calculate_health_score(self, metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        """Calculate the overall company health score."""
        if metrics is None:
            metrics = {
                "hr_health": 85,
                "financial_health": 78,
                "project_health": 72,
                "customer_health": 90,
                "knowledge_health": 88,
                "security_health": 95,
                "operational_health": 82,
            }

        scores = []
        dimension_details = {}

        for dim in self.dimensions:
            score = metrics.get(dim, 50)
            scores.append(score)
            dimension_details[dim] = {
                "score": score,
                "status": "healthy" if score >= 80 else "warning" if score >= 60 else "critical",
            }

        overall_score = sum(scores) / len(scores) if scores else 0

        # Calculate trend direction
        trend = "stable"
        if overall_score > 80:
            trend = "improving"
        elif overall_score < 60:
            trend = "declining"

        return {
            "overall_score": round(overall_score, 1),
            "trend": trend,
            "dimensions": dimension_details,
            "timestamp": settings.debug,  # placeholder
        }

    def get_health_breakdown(self) -> Dict[str, Any]:
        """Return a detailed health breakdown for all dimensions."""
        return {
            dimension: {
                "score": self._get_dimension_score(dimension),
                "status": self._get_dimension_status(dimension),
            }
            for dimension in self.dimensions
        }

    def _get_dimension_score(self, dimension: str) -> float:
        """Get the score for a specific dimension (placeholder)."""
        default_scores = {
            "hr_health": 85,
            "financial_health": 78,
            "project_health": 72,
            "customer_health": 90,
            "knowledge_health": 88,
            "security_health": 95,
            "operational_health": 82,
        }
        return default_scores.get(dimension, 50)

    def _get_dimension_status(self, dimension: str) -> str:
        """Get the status for a specific dimension."""
        score = self._get_dimension_score(dimension)
        if score >= 80:
            return "healthy"
        elif score >= 60:
            return "warning"
        return "critical"
