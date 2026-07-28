"""Agent orchestrator for coordinating multi-agent workflows."""

import asyncio
from typing import Any, Dict, List, Optional
from .base import AgentConfig, AgentResponse, BaseAgent


class AgentOrchestrator:
    """Orchestrates multiple agents to work together on complex tasks."""

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator."""
        self._agents[agent.config.name] = agent

    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Retrieve a registered agent by name."""
        return self._agents.get(name)

    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> List[AgentResponse]:
        """Execute a task across all registered agents in parallel."""
        tasks = [
            agent.process(task, context)
            for agent in self._agents.values()
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for response in responses:
            if isinstance(response, AgentResponse):
                results.append(response)
        return results

    async def sequential(self, task: str, agent_names: List[str], context: Optional[Dict[str, Any]] = None) -> List[AgentResponse]:
        """Execute a task through a sequence of agents."""
        results = []
        for name in agent_names:
            agent = self._agents.get(name)
            if agent:
                response = await agent.process(task, context)
                results.append(response)
                task = response.content  # Pass output to next agent
        return results
