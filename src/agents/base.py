"""Base agent class for the multi-agent system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AgentConfig(BaseModel):
    name: str
    description: str
    capabilities: List[str] = []
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096


class AgentResponse(BaseModel):
    agent_name: str
    content: str
    confidence: float
    sources: List[str] = []
    reasoning: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all agents in the platform."""

    def __init__(self, config: AgentConfig):
        self.config = config

    @abstractmethod
    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process input and return an agent response."""
        pass

    @abstractmethod
    async def explain(self) -> str:
        """Provide an explainable reasoning for the agent's decisions."""
        pass
