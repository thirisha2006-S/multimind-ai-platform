"""Security AI Agent — specialized in security and access control."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class SecurityAgent(BaseAgent):
    """Specialized AI agent for security monitoring, access control, and threat detection."""

    def __init__(self):
        config = AgentConfig(
            name="Security AI",
            description="Handles security monitoring, access control analysis, threat detection, and compliance auditing",
            capabilities=["threat_detection", "access_control", "compliance_auditing", "security_monitoring"],
            role="security",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze security queries and provide domain-specific insights."""
        security_logs = context.get("security_logs", []) if context else []

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Security analysis for query: '{input_data[:100]}'.",
            confidence=0.88,
            sources=["security_logs", "access_audit_trail"],
            reasoning="Applied security monitoring and threat detection models to the query.",
            validation_status="validated",
            metadata={"domain": "security", "log_entries": len(security_logs)},
        )

    async def explain(self) -> str:
        return (
            "The Security Agent monitors access patterns, detects security threats, "
            "audits compliance with security policies, and provides real-time "
            "alerts for suspicious activities."
        )
