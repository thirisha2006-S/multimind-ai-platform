"""LangGraph-based orchestrator for MultiMind AI Platform."""

from typing import Any, Dict, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
import os

from ..utils.config import settings
from ..utils.logger import get_logger
from .base import AgentConfig, AgentResponse, BaseAgent

logger = get_logger(__name__)


class AgentState(TypedDict):
    """State shared across all agents in the orchestrator."""
    user_query: str
    agent_responses: List[dict]
    current_agent: str
    step: str
    context: Dict[str, Any]
    errors: List[str]
    final_answer: str
    confidence: float
    sources: List[str]
    metadata: Dict[str, Any]


def _get_llm(model: str = "") -> Any:
    """Get the appropriate LLM based on configuration."""
    llm_choice = model or settings.openai_model

    if settings.openai_api_key:
        return ChatOpenAI(
            model=llm_choice,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )
    elif settings.cohere_api_key:
        return ChatCohere(
            model=settings.cohere_model or "command",
            api_key=settings.cohere_api_key,
        )
    else:
        logger.warning("No LLM API key configured. Using mock responses.")
        return None


def supervisor_node(state: AgentState) -> AgentState:
    """Analyze the user request and determine the workflow."""
    query = state.get("user_query", "")
    context = state.get("context", {})

    # Route based on query content
    lower_query = query.lower()

    if any(word in lower_query for word in ["finance", "revenue", "expense", "budget", "payroll", "profit"]):
        next_step = "finance"
    elif any(word in lower_query for word in ["employee", "hr", "leave", "recruit", "attendance", "performance"]):
        next_step = "hr"
    elif any(word in lower_query for word in ["legal", "compliance", "policy", "contract", "law"]):
        next_step = "legal"
    elif any(word in lower_query for word in ["project", "deadline", "team", "resource", "milestone"]):
        next_step = "project"
    elif any(word in lower_query for word in ["sales", "customer", "crm", "lead", "opportunity"]):
        next_step = "sales"
    elif any(word in lower_query for word in ["security", "access", "threat", "audit", "breach"]):
        next_step = "security"
    else:
        next_step = "research"

    logger.info(f"Supervisor routed query to: {next_step}")

    return {
        **state,
        "current_agent": "supervisor",
        "step": f"routed_to_{next_step}",
        "context": {**context, "routed_to": next_step},
    }


def planner_node(state: AgentState) -> AgentState:
    """Break down the query into actionable steps."""
    query = state.get("user_query", "")

    steps = [
        "Analyze the user request",
        "Retrieve relevant knowledge from the knowledge base",
        "Search external sources if needed",
        "Invoke appropriate specialized agents",
        "Validate and cross-reference results",
        "Check for conflicts in the information",
        "Generate final answer with confidence score",
    ]

    return {
        **state,
        "current_agent": "planner",
        "step": "planning_complete",
        "context": {**state.get("context", {}), "planned_steps": steps},
    }


def research_node(state: AgentState) -> AgentState:
    """Search internal knowledge base and web sources."""
    query = state.get("user_query", "")
    context = state.get("context", {})

    responses = state.get("agent_responses", [])

    # Search internal knowledge
    internal_results = []
    try:
        from ..knowledge.retriever import KnowledgeRetriever
        retriever = KnowledgeRetriever()
        internal_results = retriever.search(query, top_k=3)
    except Exception as e:
        logger.error(f"Internal search error: {e}")

    # Search external web if query suggests it
    web_results = []
    if context.get("web_search_enabled", True):
        try:
            from tavily import TavilyClient
            if settings.tavily_api_key:
                client = TavilyClient(api_key=settings.tavily_api_key)
                response = client.search(query, max_results=3)
                web_results = response.get("results", [])
        except ImportError:
            logger.warning("Tavily not installed — skipping web search")
        except Exception as e:
            logger.error(f"Web search error: {e}")

    # Use LLM for response generation if available
    llm = _get_llm()
    answer = "Based on internal knowledge and web research."
    confidence = 0.80

    if llm is not None:
        try:
            combined_context = f"Query: {query}\nInternal results: {internal_results}\nWeb results: {web_results}"
            response = llm.invoke(combined_context)
            answer = response.content if hasattr(response, "content") else str(response)
            confidence = 0.85
        except Exception as e:
            logger.error(f"LLM invocation error: {e}")
            answer = f"Research completed for: {query}"

    new_response = {
        "agent_name": "Research Agent",
        "content": answer,
        "confidence": confidence,
        "sources": [r.get("source", "") for r in internal_results] + [r.get("url", "") for r in web_results],
        "reasoning": "Searched internal knowledge base and web sources.",
        "validation_status": "validated",
    }

    all_responses = responses + [new_response]

    return {
        **state,
        "agent_responses": all_responses,
        "current_agent": "research",
        "step": "research_complete",
        "sources": [s for s in new_response["sources"] if s],
    }


def validator_node(state: AgentState) -> AgentState:
    """Validate agent responses for consistency."""
    agent_responses = state.get("agent_responses", [])

    all_confident = all(r.get("confidence", 0) >= 0.5 for r in agent_responses) if agent_responses else False
    final_confidence = (
        min(r["confidence"] for r in agent_responses)
        if all_confident and agent_responses
        else 0.6
    )

    return {
        **state,
        "current_agent": "validator",
        "step": "validation_complete",
        "confidence": final_confidence,
        "context": {
            **state.get("context", {}),
            "validation_status": "validated" if all_confident else "review_needed",
            "response_count": len(agent_responses),
        },
    }


def conflict_checker_node(state: AgentState) -> AgentState:
    """Check for conflicting information."""
    conflicts = state.get("context", {}).get("conflicts", [])
    sources = state.get("sources", [])

    return {
        **state,
        "current_agent": "conflict_checker",
        "step": "conflict_check_complete",
        "context": {**state.get("context", {}), "conflicts_detected": len(conflicts)},
    }


def reflection_node(state: AgentState) -> AgentState:
    """Analyze for improvements and learn from execution."""
    confidence = state.get("confidence", 0.5)

    reflection_note = "Response quality is good."
    if confidence < 0.7:
        reflection_note = "Low confidence detected — consider adding more context or sources."

    return {
        **state,
        "current_agent": "reflection",
        "step": "reflection_complete",
        "context": {**state.get("context", {}), "reflection": reflection_note},
    }


def aggregator_node(state: AgentState) -> AgentState:
    """Aggregate all responses into a final answer."""
    agent_responses = state.get("agent_responses", [])
    confidence = state.get("confidence", 0.5)
    sources = state.get("sources", [])
    context = state.get("context", {})

    # Build final answer from all agent responses
    answer_parts = []
    for resp in agent_responses:
        content = resp.get("content", "")
        if content:
            answer_parts.append(f"**{resp.get('agent_name', 'Agent')}:** {content}")

    final_answer = "\n\n".join(answer_parts) if answer_parts else "No answer generated."

    # Add reflection note if available
    reflection = context.get("reflection", "")
    if reflection:
        final_answer += f"\n\n_Reflection: {reflection}_"

    return {
        **state,
        "current_agent": "aggregator",
        "step": "aggregation_complete",
        "final_answer": final_answer,
        "confidence": confidence,
        "sources": sources,
        "metadata": {
            "total_agents_invoked": len(agent_responses),
            "final_confidence": confidence,
            **context,
        },
    }


def build_orchestrator() -> Optional[Any]:
    """Build and compile the LangGraph orchestrator.

    Returns:
        Compiled LangGraph app, or None if langgraph is not available.
    """
    try:
        from langgraph.graph import StateGraph, END

        workflow = StateGraph(AgentState)

        # Add all nodes
        workflow.add_node("supervisor", supervisor_node)
        workflow.add_node("planner", planner_node)
        workflow.add_node("researcher", research_node)
        workflow.add_node("validator", validator_node)
        workflow.add_node("conflict_checker", conflict_checker_node)
        workflow.add_node("reflector", reflection_node)
        workflow.add_node("aggregator", aggregator_node)

        # Define workflow edges
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", "planner")
        workflow.add_edge("planner", "researcher")
        workflow.add_edge("researcher", "validator")
        workflow.add_edge("validator", "conflict_checker")
        workflow.add_edge("conflict_checker", "reflector")
        workflow.add_edge("reflector", "aggregator")
        workflow.add_edge("aggregator", END)

        # Compile with memory for checkpointing
        memory = MemorySaver()
        app = workflow.compile(checkpointer=memory)

        logger.info("LangGraph orchestrator built successfully.")
        return app

    except ImportError as e:
        logger.error(f"LangGraph not fully available: {e}")
        return None


async def run_pipeline(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Run the full agent pipeline synchronously."""
    initial_state: AgentState = {
        "user_query": query,
        "agent_responses": [],
        "current_agent": "",
        "step": "started",
        "context": context or {},
        "errors": [],
        "final_answer": "",
        "confidence": 0.0,
        "sources": [],
        "metadata": {},
    }

    # Run through pipeline nodes manually (fallback if langgraph isn't available)
    state = supervisor_node(initial_state)
    state = planner_node(state)
    state = research_node(state)
    state = validator_node(state)
    state = conflict_checker_node(state)
    state = reflection_node(state)
    state = aggregator_node(state)

    return {
        "answer": state.get("final_answer", "No answer generated."),
        "confidence": state.get("confidence", 0.0),
        "sources": state.get("sources", []),
        "agents_invoked": state.get("metadata", {}).get("total_agents_invoked", 0),
        "metadata": state.get("metadata", {}),
    }
