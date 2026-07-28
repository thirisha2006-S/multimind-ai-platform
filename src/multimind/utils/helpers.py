"""Shared helper utilities for MultiMind AI Platform."""

import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def generate_id(prefix: str = "mm") -> str:
    """Generate a unique ID with a given prefix."""
    timestamp = datetime.now(timezone.utc).isoformat()
    hash_suffix = hashlib.sha256(timestamp.encode()).hexdigest()[:8]
    return f"{prefix}-{hash_suffix}"


def current_timestamp() -> str:
    """Return the current UTC timestamp as an ISO string."""
    return datetime.now(timezone.utc).isoformat()


def format_confidence(score: float) -> str:
    """Format a confidence score as a percentage string."""
    return f"{score * 100:.1f}%"


def safe_json_dumps(data: Any, indent: int = 2) -> str:
    """Serialize data to JSON string safely."""
    try:
        return json.dumps(data, indent=indent, default=str)
    except (TypeError, ValueError):
        return str(data)


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
