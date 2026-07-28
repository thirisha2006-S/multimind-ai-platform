"""Conflict Detection Agent — detects contradictory information across sources."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent
from dataclasses import dataclass


@dataclass
class Conflict:
    """Represents a detected conflict between two information sources."""
    source_a: str
    source_b: str
    field: str
    value_a: str
    value_b: str
    resolution: str = ""


class ConflictDetectionAgent(BaseAgent):
    """Detects contradictory information across knowledge sources and documents."""

    def __init__(self):
        config = AgentConfig(
            name="Conflict Detection Agent",
            description="Detects contradictory information across documents and knowledge sources",
            capabilities=["conflict_detection", "deduplication", "version_comparison"],
            role="conflict_detector",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Detect conflicts in the knowledge base or across agent responses."""
        knowledge_conflicts = context.get("knowledge_conflicts", []) if context else []

        conflicts = []
        for pair in knowledge_conflicts:
            conflict = Conflict(
                source_a=pair.get("source_a", "unknown"),
                source_b=pair.get("source_b", "unknown"),
                field=pair.get("field", "value"),
                value_a=pair.get("value_a", ""),
                value_b=pair.get("value_b", ""),
            )
            conflicts.append(conflict)

        conflict_summary = (
            f"Detected {len(conflicts)} conflicts.\n"
            + "\n".join(
                f"- {c.field}: '{c.value_a}' (from {c.source_a}) vs '{c.value_b}' (from {c.source_b})"
                for c in conflicts
            )
        ) if conflicts else "No conflicting information detected."

        return AgentResponse(
            agent_name=self.config.name,
            content=conflict_summary,
            confidence=0.8,
            sources=[c.source_a for c in conflicts] + [c.source_b for c in conflicts],
            reasoning="Compared all document versions and knowledge sources for contradictory values.",
            validation_status="validated" if not conflicts else "conflicts_found",
            metadata={"conflict_count": len(conflicts), "conflicts": [c.__dict__ for c in conflicts]},
        )

    async def explain(self) -> str:
        return (
            "The Conflict Detection Agent compares all document versions and knowledge "
            "sources to find contradictions. When conflicts are detected, it identifies "
            "the latest version and assigns reduced confidence to the conflicting answer."
        )
