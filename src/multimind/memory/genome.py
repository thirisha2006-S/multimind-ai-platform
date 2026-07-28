"""Company Knowledge Genome for MultiMind AI Platform.

The Knowledge Genome learns the organization's unique patterns including:
- Decision patterns and business strategies
- Approval workflows and team collaboration styles
- Company culture and successful/failed project patterns
- Customer behavior and risk tolerance

This creates organization-specific intelligence that goes beyond generic AI knowledge.
"""

import sqlite3
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..utils.config import settings
from ..utils.helpers import generate_id, current_timestamp


class KnowledgeGenomeEntry:
    """A single entry in the Company Knowledge Genome."""

    def __init__(
        self,
        pattern_type: str,
        pattern_key: str,
        pattern_data: Dict[str, Any],
        confidence: float = 0.5,
    ):
        self.id = generate_id("genome")
        self.pattern_type = pattern_type  # e.g., "decision_pattern", "approval_workflow", "team_collaboration"
        self.pattern_key = pattern_key
        self.pattern_data = pattern_data
        self.confidence = confidence
        self.created_at = current_timestamp()
        self.updated_at = self.created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pattern_type": self.pattern_type,
            "pattern_key": self.pattern_key,
            "pattern_data": self.pattern_data,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class KnowledgeGenome:
    """The Company Knowledge Genome — learns and remembers organization-specific patterns."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or (settings.database_url.replace("sqlite:///", "") + "_genome")
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the genome database schema."""
        import os

        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_genome (
                id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                pattern_key TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def record_decision(self, decision_name: str, decision_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record a company decision pattern."""
        entry = KnowledgeGenomeEntry(
            pattern_type="decision_pattern",
            pattern_key=decision_name,
            pattern_data=decision_data,
            confidence=0.8,
        )
        self._save(entry)
        return entry

    def record_approval_workflow(self, workflow_name: str, workflow_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record an approval workflow pattern."""
        entry = KnowledgeGenomeEntry(
            pattern_type="approval_workflow",
            pattern_key=workflow_name,
            pattern_data=workflow_data,
            confidence=0.75,
        )
        self._save(entry)
        return entry

    def record_team_collaboration(self, team_name: str, collab_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record a team collaboration pattern."""
        entry = KnowledgeGenomeEntry(
            pattern_type="team_collaboration",
            pattern_key=team_name,
            pattern_data=collab_data,
            confidence=0.7,
        )
        self._save(entry)
        return entry

    def record_project_outcome(self, project_name: str, outcome_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record a project outcome (success or failure) pattern."""
        entry = KnowledgeGenomeEntry(
            pattern_type="project_outcome",
            pattern_key=project_name,
            pattern_data=outcome_data,
            confidence=0.85 if outcome_data.get("success") else 0.6,
        )
        self._save(entry)
        return entry

    def record_customer_behavior(self, behavior_key: str, behavior_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record customer behavior patterns."""
        entry = KnowledgeGenomeEntry(
            pattern_type="customer_behavior",
            pattern_key=behavior_key,
            pattern_data=behavior_data,
            confidence=0.7,
        )
        self._save(entry)
        return entry

    def record_risk_profile(self, risk_name: str, risk_data: Dict[str, Any]) -> KnowledgeGenomeEntry:
        """Record the organization's risk tolerance patterns."""
        entry = KnowledgeGenomeEntry(
            pattern_type="risk_profile",
            pattern_key=risk_name,
            pattern_data=risk_data,
            confidence=0.75,
        )
        self._save(entry)
        return entry

    def search_pattern(self, pattern_type: str, pattern_key: str) -> Optional[KnowledgeGenomeEntry]:
        """Search for a specific genome pattern."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, pattern_type, pattern_key, pattern_data, confidence, created_at, updated_at FROM knowledge_genome WHERE pattern_type = ? AND pattern_key = ?",
            (pattern_type, pattern_key),
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        entry = KnowledgeGenomeEntry(
            pattern_type=row[1],
            pattern_key=row[2],
            pattern_data=json.loads(row[3]),
            confidence=row[4],
        )
        entry.id = row[0]
        entry.created_at = row[5]
        entry.updated_at = row[6]
        return entry

    def get_patterns_by_type(self, pattern_type: str) -> List[KnowledgeGenomeEntry]:
        """Retrieve all patterns of a specific type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, pattern_type, pattern_key, pattern_data, confidence, created_at, updated_at FROM knowledge_genome WHERE pattern_type = ?",
            (pattern_type,),
        )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = KnowledgeGenomeEntry(
                pattern_type=row[1],
                pattern_key=row[2],
                pattern_data=json.loads(row[3]),
                confidence=row[4],
            )
            entry.id = row[0]
            entry.created_at = row[5]
            entry.updated_at = row[6]
            entries.append(entry)

        return entries

    def get_all_patterns(self) -> List[KnowledgeGenomeEntry]:
        """Retrieve all genome patterns."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, pattern_type, pattern_key, pattern_data, confidence, created_at, updated_at FROM knowledge_genome"
        )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = KnowledgeGenomeEntry(
                pattern_type=row[1],
                pattern_key=row[2],
                pattern_data=json.loads(row[3]),
                confidence=row[4],
            )
            entry.id = row[0]
            entry.created_at = row[5]
            entry.updated_at = row[6]
            entries.append(entry)

        return entries

    def get_health_report(self) -> Dict[str, Any]:
        """Generate a health report of the Knowledge Genome."""
        all_patterns = self.get_all_patterns()
        by_type: Dict[str, int] = {}
        by_confidence: Dict[str, List[float]] = {}

        for pattern in all_patterns:
            by_type[pattern.pattern_type] = by_type.get(pattern.pattern_type, 0) + 1
            if pattern.pattern_type not in by_confidence:
                by_confidence[pattern.pattern_type] = []
            by_confidence[pattern.pattern_type].append(pattern.confidence)

        avg_confidence = {}
        for ptype, confidences in by_confidence.items():
            avg_confidence[ptype] = sum(confidences) / len(confidences) if confidences else 0.0

        return {
            "total_patterns": len(all_patterns),
            "pattern_types": by_type,
            "average_confidence_by_type": avg_confidence,
            "overall_confidence": (
                sum(c.confidence for c in all_patterns) / len(all_patterns) if all_patterns else 0.0
            ),
        }

    def _save(self, entry: KnowledgeGenomeEntry) -> None:
        """Save a genome entry to the database."""
        import os

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO knowledge_genome (id, pattern_type, pattern_key, pattern_data, confidence, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.id,
                entry.pattern_type,
                entry.pattern_key,
                json.dumps(entry.pattern_data, default=str),
                entry.confidence,
                entry.created_at,
                entry.updated_at,
            ),
        )
        conn.commit()
        conn.close()
