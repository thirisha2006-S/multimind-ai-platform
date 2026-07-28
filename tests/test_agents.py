"""Tests for agent system."""

import pytest
from src.agents.base import AgentConfig, AgentResponse, BaseAgent


class MockAgent(BaseAgent):
    """A mock agent for testing."""

    async def process(self, input_data, context=None):
        return AgentResponse(
            agent_name=self.config.name,
            content=f"Processed: {input_data}",
            confidence=0.95,
        )

    async def explain(self):
        return "Mock agent processes input with predefined logic."


@pytest.fixture
def mock_agent():
    config = AgentConfig(name="mock", description="Mock agent")
    return MockAgent(config)


@pytest.mark.asyncio
async def test_mock_agent_process(mock_agent):
    response = await mock_agent.process("hello")
    assert response.agent_name == "mock"
    assert response.confidence == 0.95
    assert "hello" in response.content


@pytest.mark.asyncio
async def test_mock_agent_explain(mock_agent):
    explanation = await mock_agent.explain()
    assert "Mock agent" in explanation