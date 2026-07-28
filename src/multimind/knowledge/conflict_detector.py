"""Knowledge conflict detection for MultiMind AI Platform."""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from ..utils.helpers import current_timestamp


@dataclass
class KnowledgeConflict:
    """Represents a detected conflict in the knowledge base."""
    field: str
    value_a: str
    value_b: str
    source_a: str
    source_b: str
    detected_at: str = ""
    resolution: str = "pending"

    def __post_init__(self):
        if not self.detected_at:
            self.detected_at = current_timestamp()


class ConflictDetector:
    """Detects conflicting information across knowledge sources and document versions."""

    def __init__(self):
        self.conflicts: List[KnowledgeConflict] = []

    def detect(self, documents: List[Dict[str, Any]]) -> List[KnowledgeConflict]:
        """Detect conflicts across a collection of documents."""
        self.conflicts = []

        # Group documents by field name
        field_values: Dict[str, List[Dict[str, Any]]] = {}
        for doc in documents:
            for field, value in doc.items():
                if field not in field_values:
                    field_values[field] = []
                field_values[field].append({
                    "value": value,
                    "source": doc.get("source", "unknown"),
                    "version": doc.get("version", "unknown"),
                })

        # Check for conflicts (same field, different values)
        for field, entries in field_values.items():
            values = set(str(e["value"]) for e in entries)
            if len(values) > 1:
                # Conflict detected
                sorted_entries = sorted(entries, key=lambda e: e.get("version", ""))
                latest = sorted_entries[-1]
                older = sorted_entries[:-1]

                for older_entry in older:
                    conflict = KnowledgeConflict(
                        field=field,
                        value_a=str(latest["value"]),
                        value_b=str(older_entry["value"]),
                        source_a=latest.get("source", "unknown"),
                        source_b=older_entry.get("source", "unknown"),
                    )
                    conflict.resolution = "latest_wins"
                    self.conflicts.append(conflict)

        return self.conflicts

    def get_conflicts(self) -> List[KnowledgeConflict]:
        """Return all detected conflicts."""
        return self.conflicts

    def resolve_conflict(self, conflict: KnowledgeConflict, resolution: str) -> None:
        """Resolve a specific conflict with a given resolution."""
        conflict.resolution = resolution

    async def suggest_resolution(self, conflict: KnowledgeConflict) -> str:
        """Suggest a resolution for a conflict based on document freshness."""
        return f"Use value from {conflict.source_a} (latest version) and archive {conflict.source_b}"
