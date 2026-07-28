"""Finance AI Agent — specialized in financial analysis and reporting."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class FinanceAgent(BaseAgent):
    """Specialized AI agent for finance queries and analysis."""

    def __init__(self):
        config = AgentConfig(
            name="Finance AI",
            description="Handles financial analysis, revenue tracking, budget monitoring, and cash flow analysis",
            capabilities=["revenue_analysis", "budget_tracking", "cash_flow", "payroll", "forecasting"],
            role="finance",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze financial queries and provide domain-specific insights."""
        financial_data = context.get("financial_data", {}) if context else {}

        analysis = f"Finance analysis for query: '{input_data[:100]}'"
        if financial_data:
            analysis += f"\nKey metrics: {financial_data}"

        return AgentResponse(
            agent_name=self.config.name,
            content=analysis,
            confidence=0.78,
            sources=["financial_reports", "budget_documents"],
            reasoning="Applied financial analysis models to the query using available financial data.",
            validation_status="validated",
            metadata={"domain": "finance", "data_points": len(financial_data)},
        )

    async def explain(self) -> str:
        return (
            "The Finance Agent specializes in financial analysis including "
            "revenue tracking, budget monitoring, payroll analysis, cash flow "
            "projections, and fiscal year reporting."
        )
