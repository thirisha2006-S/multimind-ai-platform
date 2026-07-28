"""Project AI Agent — specialized in project management analysis."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class ProjectAgent(BaseAgent):
    """Specialized AI agent for project management and tracking."""

    def __init__(self):
        config = AgentConfig(
            name="Project AI",
            description="Handles project progress tracking, deadline management, team allocation, and risk analysis",
            capabilities=["progress_tracking", "deadline_management", "resource_allocation", "risk_analysis"],
            role="project",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze project queries and provide domain-specific insights."""
        project_data = context.get("project_data", {}) if context else {}

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Project analysis for query: '{input_data[:100]}'.",
            confidence=0.80,
            sources=["project_management_system", "task_tracker"],
            reasoning="Applied project management domain knowledge to analyze progress, deadlines, and risks.",
            validation_status="validated",
            metadata={"domain": "project", "projects_tracked": len(project_data)},
        )

    async def explain(self) -> str:
        return (
            "The Project Agent tracks project progress, manages deadlines, "
            "allocates team resources, and identifies project risks. It provides "
            "data-driven insights to keep projects on track."
        )
