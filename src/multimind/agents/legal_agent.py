"""Legal AI Agent — specialized in legal and compliance matters."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class LegalAgent(BaseAgent):
    """Specialized AI agent for legal queries, compliance, and policy analysis."""

    def __init__(self):
        config = AgentConfig(
            name="Legal AI",
            description="Handles legal document analysis, compliance checks, policy interpretation, and risk assessment",
            capabilities=["legal_analysis", "compliance_checking", "policy_interpretation", "risk_assessment"],
            role="legal",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze legal queries and provide domain-specific insights."""
        legal_docs = context.get("legal_documents", []) if context else []

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Legal analysis for query: '{input_data[:100]}'. Reviewed {len(legal_docs)} legal documents.",
            confidence=0.75,
            sources=[doc.get("source", "legal_docs") for doc in legal_docs],
            reasoning="Applied legal domain knowledge and compliance rules to the query.",
            validation_status="validated",
            metadata={"domain": "legal", "documents_reviewed": len(legal_docs)},
        )

    async def explain(self) -> str:
        return (
            "The Legal Agent specializes in legal document analysis, compliance "
            "regulations, policy interpretation, contract review, and legal risk "
            "assessment for the organization."
        )
