"""Reflection Agent — improves future responses by learning from previous executions."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class ReflectionAgent(BaseAgent):
    """Improves future responses by learning from previous execution patterns."""

    def __init__(self):
        config = AgentConfig(
            name="Reflection Agent",
            description="Learns from previous agent executions to improve future responses",
            capabilities=["pattern_recognition", "performance_analysis", "self_improvement"],
            role="reflection",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze previous executions and identify improvement opportunities."""
        execution_history = context.get("execution_history", []) if context else []

        improvement_areas = []
        for exec_record in execution_history[-5:]:  # Last 5 executions
            if exec_record.get("confidence", 0) < 0.7:
                improvement_areas.append(exec_record.get("agent_name", "unknown"))

        if improvement_areas:
            improvement_text = (
                f"Reflection analysis identified that agents {improvement_areas} "
                "had lower confidence in recent executions. Consider adjusting "
                "retrieval parameters or adding additional training examples."
            )
        else:
            improvement_text = "Recent executions show high confidence. No improvements needed at this time."

        return AgentResponse(
            agent_name=self.config.name,
            content=improvement_text,
            confidence=0.85,
            sources=execution_history,
            reasoning="Analyzed last 5 execution records for confidence patterns and improvement areas.",
            validation_status="validated",
            metadata={"history_analyzed": len(execution_history[-5:]), "issues_found": len(improvement_areas)},
        )

    async def explain(self) -> str:
        return (
            "The Reflection Agent maintains a learning loop by analyzing past agent "
            "executions. It identifies patterns of low confidence, knowledge gaps, "
            "and workflow inefficiencies, then recommends improvements for future runs."
        )
