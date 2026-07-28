"""Base agent classes for the MultiMind AI multi-agent system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an AI agent."""
    name: str
    description: str
    capabilities: List[str] = Field(default_factory=list)
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    role: str = "general"


class AgentResponse(BaseModel):
    """Standard response from any agent."""
    agent_name: str
    content: str
    confidence: float = 0.0
    sources: List[str] = Field(default_factory=list)
    reasoning: Optional[str] = None
    validation_status: str = "pending"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all agents in the MultiMind AI platform."""

    def __init__(self, config: AgentConfig):
        self.config = config

    @abstractmethod
    async def process(self, input_data: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process input and return an agent response."""
        pass

    @abstractmethod
    async def explain(self) -> str:
        """Provide explainable reasoning for the agent's decisions."""
        pass

    def get_capabilities(self) -> List[str]:
        """Return the agent's capabilities."""
        return self.config.capabilities

    def get_confidence(self) -> str:
        """Format the agent's confidence level."""
        from ..utils.helpers import format_confidence
        return format_confidence(self.config.temperature)
