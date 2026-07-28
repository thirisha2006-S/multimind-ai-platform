"""Supervisor Agent — controls the workflow across all specialized agents."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class SupervisorAgent(BaseAgent):
    """Controls the workflow by delegating tasks to specialized agents."""

    def __init__(self):
        config = AgentConfig(
            name="Supervisor Agent",
            description="Controls the multi-agent workflow and delegates tasks to specialized agents",
            capabilities=["workflow_management", "task_delegation", "priority_routing"],
            role="supervisor",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze the request and determine which agents to invoke."""
        agent_list = context.get("agent_list", []) if context else []

        reasoning = (
            f"Supervisor Agent analyzed the request and determined the following "
            f"workflow: {[a.config.name for a in agent_list]}."
        )

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Workflow orchestrated for request: {input_data[:200]}",
            confidence=0.9,
            sources=[],
            reasoning=reasoning,
            validation_status="approved",
            metadata={"delegated_agents": [a.config.name for a in agent_list]},
        )

    async def explain(self) -> str:
        return (
            "The Supervisor Agent analyzes user requests and determines which "
            "specialized agents are needed. It manages the workflow by delegating "
            "tasks and aggregating results from each agent."
        )
