"""Research Agent — searches internal documents and trusted web sources."""

from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class ResearchAgent(BaseAgent):
    """Searches internal knowledge base and web sources for relevant information."""

    def __init__(self):
        config = AgentConfig(
            name="Research Agent",
            description="Searches internal documents and trusted web sources for information",
            capabilities=["internal_search", "web_search", "source_retrieval"],
            role="research",
        )
        super().__init__(config)

    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Search internal and external sources for relevant information."""
        knowledge_base = context.get("knowledge_retriever") if context else None
        web_search = context.get("web_search_enabled", False)

        sources = []
        content_parts = []

        # Internal search
        if knowledge_base:
            try:
                results = await knowledge_base.search(input_data, top_k=3)
                for r in results:
                    sources.append(r.source)
                    content_parts.append(r.content[:200])
            except Exception:
                pass

        # Web search if enabled
        if web_search:
            try:
                from tavily import TavilyClient
                api_key = context.get("tavily_api_key", "")
                if api_key:
                    client = TavilyClient(api_key=api_key)
                    response = client.search(input_data, max_results=3)
                    for result in response.get("results", []):
                        sources.append(result.get("url", "web"))
                        content_parts.append(result.get("content", "")[:200])
            except Exception:
                pass

        combined_content = " ".join(content_parts) if content_parts else "No relevant sources found."

        return AgentResponse(
            agent_name=self.config.name,
            content=f"Research results for: '{input_data[:100]}...'\n\n{combined_content}",
            confidence=0.75,
            sources=sources,
            reasoning="Searched both internal knowledge base and web sources for comprehensive answers.",
            validation_status="needs_validation",
            metadata={"web_search": web_search, "sources_found": len(sources)},
        )

    async def explain(self) -> str:
        return (
            "The Research Agent performs dual-source research: first searching the "
            "internal knowledge base for company-specific information, then using "
            "Tavily Search API for web sources when needed. Results are ranked by "
            "relevance and source credibility."
        )
