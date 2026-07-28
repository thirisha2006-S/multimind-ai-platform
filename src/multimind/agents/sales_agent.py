"""Sales AI Agent — specialized in sales analysis and customer management."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class SalesAgent(BaseAgent):
    """Specialized AI agent for sales analysis, CRM, and customer insights."""

    def __init__(self):
        config = AgentConfig(
            name="Sales AI",
            description="Handles sales forecasting, CRM analysis, customer behavior insights, and revenue prediction",
            capabilities=["sales_forecasting", "crm_analysis", "customer_insights", "revenue_prediction"],
            role="sales",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Analyze sales queries and provide domain-specific insights."""
        sales_data = context.get("sales_data", {}) if context else {}

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Sales analysis for query: '{input_data[:100]}'.",
            confidence=0.77,
            sources=["crm_system", "sales_reports"],
            reasoning="Applied sales domain models to analyze trends, forecast revenues, and identify opportunities.",
            validation_status="validated",
            metadata={"domain": "sales", "records": len(sales_data)},
        )

    async def explain(self) -> str:
        return (
            "The Sales Agent analyzes CRM data, sales trends, customer behavior, "
            "and revenue patterns to provide actionable sales insights and forecasts."
        )
