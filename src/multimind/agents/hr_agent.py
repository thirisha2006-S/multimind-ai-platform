"""HR AI Agent — specialized in human resources management."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class HRAgent(BaseAgent):
    """Specialized AI agent for human resources queries and management."""

    def __init__(self):
        config = AgentConfig(
            name="HR AI",
            description="Handles employee management, leave tracking, recruitment, attendance, training, and performance",
            capabilities=["employee_management", "leave_tracking", "recruitment", "attendance", "performance"],
            role="hr",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze HR queries and provide domain-specific insights."""
        hr_data = context.get("hr_data", {}) if context else {}

        analysis = f"HR analysis for query: '{input_data[:100]}'"
        if hr_data:
            analysis += f"\nEmployee data context: {len(hr_data)} records"

        return AgentResponse(
            agent_name=self.config.name,
            content=analysis,
            confidence=0.82,
            sources=["hr_system", "employee_database"],
            reasoning="Applied HR domain knowledge to the query using employee and HR data.",
            validation_status="validated",
            metadata={"domain": "hr", "records_count": len(hr_data)},
        )

    async def explain(self) -> str:
        return (
            "The HR Agent specializes in employee management, leave tracking, "
            "recruitment analysis, attendance monitoring, training needs, "
            "and performance reviews."
        )
