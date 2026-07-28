"""Audit logging for MultiMind AI Platform."""

import json
import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from ..utils.config import settings


class AuditLogEntry:
    """A single audit log entry."""

    def __init__(
        self,
        user_id: str,
        action: str,
        resource: str,
        details: Dict[str, Any],
        success: bool = True,
        ip_address: str = "127.0.0.1",
    ):
        self.id = hashlib.sha256(f"{user_id}{action}{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:16]
        self.user_id = user_id
        self.action = action
        self.resource = resource
        self.details = details
        self.success = success
        self.ip_address = ip_address
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource": self.resource,
            "details": self.details,
            "success": self.success,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp,
        }


import hashlib


class AuditLogger:
    """Centralized audit logging for all MultiMind AI operations."""

    def __init__(self):
        self._db_path = settings.database_url.replace("sqlite:///", "") + "_audit"
        self._init_db()

    def _init_db(self) -> None:
        """Initialize audit log database."""
        import os

        db_dir = os.path.dirname(self._db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                resource TEXT NOT NULL,
                details TEXT NOT NULL,
                success INTEGER NOT NULL DEFAULT 1,
                ip_address TEXT DEFAULT '127.0.0.1',
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def log(self, user_id: str, action: str, resource: str, details: Dict[str, Any] = None, success: bool = True) -> AuditLogEntry:
        """Log an audit entry."""
        entry = AuditLogEntry(
            user_id=user_id,
            action=action,
            resource=resource,
            details=details or {},
            success=success,
        )

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_log (id, user_id, action, resource, details, success, ip_address, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entry.id,
                entry.user_id,
                entry.action,
                entry.resource,
                json.dumps(entry.details),
                1 if entry.success else 0,
                entry.ip_address,
                entry.timestamp,
            ),
        )
        conn.commit()
        conn.close()

        return entry

    def log_login(self, user_id: str, success: bool = True) -> AuditLogEntry:
        """Log a user login event."""
        return self.log(user_id, "login", "authentication", {"success": success})

    def log_query(self, user_id: str, query: str, success: bool = True) -> AuditLogEntry:
        """Log an AI query."""
        return self.log(user_id, "ai_query", "ai_engine", {"query": query[:200]})

    def log_data_access(self, user_id: str, resource: str, success: bool = True) -> AuditLogEntry:
        """Log a data access event."""
        return self.log(user_id, "data_access", resource, {"authorized": True})

    def get_logs(self, user_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve audit logs, optionally filtered by user."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        if user_id:
            cursor.execute(
                "SELECT id, user_id, action, resource, details, success, ip_address, timestamp FROM audit_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            cursor.execute(
                "SELECT id, user_id, action, resource, details, success, ip_address, timestamp FROM audit_log ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            )
        rows = cursor.fetchall()
        conn.close()

        logs = []
        for row in rows:
            logs.append(
                {
                    "id": row[0],
                    "user_id": row[1],
                    "action": row[2],
                    "resource": row[3],
                    "details": json.loads(row[4]),
                    "success": bool(row[5]),
                    "ip_address": row[6],
                    "timestamp": row[7],
                }
            )
        return logs
