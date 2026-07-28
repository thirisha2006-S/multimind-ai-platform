"""Planner Agent — breaks complex tasks into smaller actionable steps."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class PlannerAgent(BaseAgent):
    """Breaks complex tasks into smaller, manageable steps."""

    def __init__(self):
        config = AgentConfig(
            name="Planner Agent",
            description="Decomposes complex user requests into structured action plans",
            capabilities=["task_decomposition", "planning", "sequencing"],
            role="planner",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Decompose the input task into steps."""
        steps = [
            f"Step 1: Understand the request — '{input_data[:100]}'",
            "Step 2: Identify relevant internal knowledge",
            "Step 3: Identify external sources if needed",
            "Step 4: Delegate to specialized agents",
            "Step 5: Validate and aggregate results",
            "Step 6: Deliver final response with explanations",
        ]

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Task decomposed into {len(steps)} steps:\n" + "\n".join(f"- {s}" for s in steps),
            confidence=0.85,
            sources=[],
            reasoning="Complex requests require structured decomposition for accuracy.",
            validation_status="approved",
            metadata={"step_count": len(steps), "original_input": input_data[:200]},
        )

    async def explain(self) -> str:
        return (
            "The Planner Agent decomposes complex user requests into sequential, "
            "manageable steps. This ensures that multi-faceted questions are "
            "handled systematically and no important aspects are missed."
        )
