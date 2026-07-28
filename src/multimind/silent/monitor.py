"""Silent AI Monitoring for MultiMind AI Platform.

Proactively detects problems instead of waiting for user questions.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timezone

from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Alert:
    """A proactive alert from the Silent AI system."""
    alert_type: str  # 'project_delay', 'customer_churn', 'budget_overrun', etc.
    message: str
    severity: str = "warning"  # info, warning, critical
    timestamp: str = ""
    acknowledged: bool = False

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


class SilentMonitor:
    """Proactively detects problems and alerts users."""

    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_history: List[Alert] = []

    def check_project_delays(self, projects: List[Dict[str, Any]] = None) -> List[Alert]:
        """Check for project delays and generate alerts."""
        new_alerts = []
        projects = projects or []

        for project in projects:
            status = project.get("status", "on_track")
            if status == "delayed":
                alert = Alert(
                    alert_type="project_delay",
                    message=f"Project '{project.get('name', 'Unknown')}' is delayed.",
                    severity="warning",
                )
                new_alerts.append(alert)
                self.alerts.append(alert)

        return new_alerts

    def check_customer_churn_risk(self, customers: List[Dict[str, Any]] = None) -> List[Alert]:
        """Check for customer churn risks."""
        new_alerts = []
        customers = customers or []

        for customer in customers:
            risk_score = customer.get("churn_risk_score", 0)
            if risk_score > 0.7:
                alert = Alert(
                    alert_type="customer_churn",
                    message=f"Customer '{customer.get('name', 'Unknown')}' at high churn risk (score: {risk_score:.0%}).",
                    severity="critical",
                )
                new_alerts.append(alert)
                self.alerts.append(alert)

        return new_alerts

    def check_budget_overruns(self, departments: List[Dict[str, Any]] = None) -> List[Alert]:
        """Check for budget overruns."""
        new_alerts = []
        departments = departments or []

        for dept in departments:
            budget = dept.get("budget", 0)
            spent = dept.get("spent", 0)
            utilization = spent / budget if budget > 0 else 0

            if utilization > 0.9:
                alert = Alert(
                    alert_type="budget_overrun",
                    message=f"Department '{dept.get('name', 'Unknown')}' budget at {utilization:.0%} utilization.",
                    severity="warning" if utilization < 1.0 else "critical",
                )
                new_alerts.append(alert)
                self.alerts.append(alert)

        return new_alerts

    def run_full_monitoring(self, data: Dict[str, Any] = None) -> List[Alert]:
        """Run all monitoring checks and return new alerts."""
        all_new_alerts = []

        data = data or {}

        all_new_alerts.extend(self.check_project_delays(data.get("projects", [])))
        all_new_alerts.extend(self.check_customer_churn_risk(data.get("customers", [])))
        all_new_alerts.extend(self.check_budget_overruns(data.get("departments", [])))

        return all_new_alerts

    def get_active_alerts(self) -> List[Alert]:
        """Return all unacknowledged alerts."""
        return [a for a in self.alerts if not a.acknowledged]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a specific alert."""
        for alert in self.alerts:
            if alert.alert_type == alert_id or alert.timestamp == alert_id:
                alert.acknowledged = True
                self.alert_history.append(alert)
                self.alerts.remove(alert)
                return True
        return False

    def get_alert_summary(self) -> Dict[str, Any]:
        """Get a summary of all alerts."""
        active = self.get_active_alerts()
        return {
            "total_alerts": len(self.alerts) + len(self.alert_history),
            "active_alerts": len(active),
            "acknowledged_alerts": len(self.alert_history),
            "by_severity": {
                "critical": sum(1 for a in active if a.severity == "critical"),
                "warning": sum(1 for a in active if a.severity == "warning"),
                "info": sum(1 for a in active if a.severity == "info"),
            },
        }
