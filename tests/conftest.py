"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_agent_config():
    """Return a sample agent configuration for testing."""
    from src.agents.base import AgentConfig
    return AgentConfig(
        name="test-agent",
        description="A test agent",
        capabilities=["test"],
        model="gpt-4o",
        temperature=0.0,
    )