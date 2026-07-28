"""Organizational memory store for MultiMind AI Platform."""

import sqlite3
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..utils.config import settings
from ..utils.helpers import generate_id, current_timestamp


class MemoryEntry:
    """A single entry in the organizational memory."""

    def __init__(
        self,
        key: str,
        value: Any,
        category: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.id = generate_id("mem")
        self.key = key
        self.value = value
        self.category = category
        self.metadata = metadata or {}
        self.created_at = current_timestamp()
        self.updated_at = self.created_at
        self.expires_at = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "category": self.category,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expires_at": self.expires_at,
        }


class MemoryStore:
    """Persistent store for organizational memory using SQLite."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the memory database schema."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True) if os.path.dirname(self.db_path) else None
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                metadata TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                expires_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def store(self, key: str, value: Any, category: str = "general", metadata: Optional[Dict[str, Any]] = None) -> MemoryEntry:
        """Store a memory entry."""
        import os

        entry = MemoryEntry(key=key, value=value, category=category, metadata=metadata)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO memory (id, key, value, category, metadata, created_at, updated_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.id,
                entry.key,
                json.dumps(entry.value, default=str),
                entry.category,
                json.dumps(entry.metadata),
                entry.created_at,
                entry.updated_at,
                entry.expires_at,
            ),
        )
        conn.commit()
        conn.close()

        return entry

    def retrieve(self, key: str) -> Optional[MemoryEntry]:
        """Retrieve a memory entry by key."""
        import os

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, key, value, category, metadata, created_at, updated_at, expires_at FROM memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        entry = MemoryEntry(
            key=row[1],
            value=json.loads(row[2]),
            category=row[3],
            metadata=json.loads(row[4]),
        )
        entry.id = row[0]
        entry.created_at = row[5]
        entry.updated_at = row[6]
        entry.expires_at = row[7]
        return entry

    def search(self, query: str, category: Optional[str] = None) -> List[MemoryEntry]:
        """Search memory entries by key containing the query string."""
        import os

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute(
                "SELECT id, key, value, category, metadata, created_at, updated_at, expires_at FROM memory WHERE key LIKE ? AND category = ?",
                (f"%{query}%", category),
            )
        else:
            cursor.execute(
                "SELECT id, key, value, category, metadata, created_at, updated_at, expires_at FROM memory WHERE key LIKE ?",
                (f"%{query}%",),
            )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = MemoryEntry(
                key=row[1],
                value=json.loads(row[2]),
                category=row[3],
                metadata=json.loads(row[4]),
            )
            entry.id = row[0]
            entry.created_at = row[5]
            entry.updated_at = row[6]
            entry.expires_at = row[7]
            entries.append(entry)

        return entries

    def delete(self, key: str) -> bool:
        """Delete a memory entry by key."""
        import os

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memory WHERE key = ?", (key,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    def get_all(self, category: Optional[str] = None) -> List[MemoryEntry]:
        """Retrieve all memory entries, optionally filtered by category."""
        import os

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute("SELECT id, key, value, category, metadata, created_at, updated_at, expires_at FROM memory WHERE category = ?", (category,))
        else:
            cursor.execute("SELECT id, key, value, category, metadata, created_at, updated_at, expires_at FROM memory")
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry = MemoryEntry(
                key=row[1],
                value=json.loads(row[2]),
                category=row[3],
                metadata=json.loads(row[4]),
            )
            entry.id = row[0]
            entry.created_at = row[5]
            entry.updated_at = row[6]
            entry.expires_at = row[7]
            entries.append(entry)

        return entries
