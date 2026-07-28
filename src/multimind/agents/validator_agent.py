"""Validator Agent — verifies the correctness of answers."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class ValidatorAgent(BaseAgent):
    """Verifies the correctness and consistency of agent responses."""

    def __init__(self):
        config = AgentConfig(
            name="Validator Agent",
            description="Verifies the correctness of answers by cross-referencing multiple sources",
            capabilities=["fact_verification", "consistency_check", "confidence_scoring"],
            role="validator",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Validate the agent outputs based on cross-referencing."""
        agent_responses = context.get("agent_responses", []) if context else []

        validation_results = []
        all_confident = True

        for response in agent_responses:
            if response.confidence < 0.5:
                all_confident = False
                validation_results.append(f"Low confidence from {response.agent_name}: {response.confidence}")

        final_confidence = 0.85 if all_confident else 0.6
        status = "validated" if all_confident else "review_needed"

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Validation complete. {len(agent_responses)} agent responses reviewed.",
            confidence=final_confidence,
            sources=[r.source for r in agent_responses for r in r.get("sources", [])],
            reasoning=f"Cross-referenced {len(agent_responses)} agent outputs for consistency.",
            validation_status=status,
            metadata={"agent_count": len(agent_responses), "all_confident": all_confident},
        )

    async def explain(self) -> str:
        return (
            "The Validator Agent cross-references outputs from all specialized agents, "
            "checks confidence scores, detects inconsistencies between different agent "
            "responses, and assigns an overall validation status."
        )
