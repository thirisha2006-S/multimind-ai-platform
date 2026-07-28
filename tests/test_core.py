"""Tests for core configuration and utilities."""

import pytest


def test_settings_defaults():
    """Test that settings load with default values."""
    from src.core.config import Settings
    settings = Settings(debug=False)
    assert settings.app_name == "Multimind AI Platform"
    assert settings.environment == "development"
    assert settings.port == 8000


def test_settings_custom():
    """Test that settings can be overridden."""
    from src.core.config import Settings
    settings = Settings(
        debug=True,
        host="127.0.0.1",
        port=9000,
        environment="testing",
    )
    assert settings.debug is True
    assert settings.host == "127.0.0.1"
    assert settings.port == 9000
    assert settings.environment == "testing"