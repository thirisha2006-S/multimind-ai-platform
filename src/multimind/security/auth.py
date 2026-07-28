"""Authentication and Role-Based Access Control (RBAC) for MultiMind AI."""

import hashlib
import sqlite3
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from ..utils.config import settings


class User:
    """Represents an authenticated user."""

    def __init__(
        self,
        user_id: str,
        username: str,
        role: str,
        email: str = "",
        department: str = "",
    ):
        self.user_id = user_id
        self.username = username
        self.role = role  # 'ceo', 'hr', 'finance', 'project_manager', 'employee'
        self.email = email
        self.department = department

    def can_access(self, resource: str) -> bool:
        """Check if the user can access a specific resource based on role."""
        role_permissions = {
            "ceo": ["*"],  # Full access
            "hr": ["hr", "employee", "training", "performance", "recruitment"],
            "finance": ["finance", "revenue", "expenses", "budget", "payroll", "cash_flow"],
            "project_manager": ["project", "team", "deadline", "risk", "progress"],
            "employee": ["tasks", "documents", "leave", "own_data", "ai_assistant"],
        }
        permissions = role_permissions.get(self.role, [])
        return "*" in permissions or resource in permissions


class Authenticator:
    """Handles user authentication and session management."""

    def __init__(self):
        self._db_path = settings.database_url.replace("sqlite:///", "") + "_auth"
        self._init_db()

    def _init_db(self) -> None:
        """Initialize authentication database."""
        import os

        db_dir = os.path.dirname(self._db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT DEFAULT '',
                department TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 (use stronger hashing in production)."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str, role: str, email: str = "", department: str = "") -> User:
        """Register a new user."""
        user_id = hashlib.sha256(f"{username}{datetime.now(timezone.utc).isoformat()}".encode()).hexdigest()[:16]
        password_hash = self.hash_password(password)
        created_at = datetime.now(timezone.utc).isoformat()

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, username, password_hash, role, email, department, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, password_hash, role, email, department, created_at),
        )
        conn.commit()
        conn.close()

        return User(user_id=user_id, username=username, role=role, email=email, department=department)

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        password_hash = self.hash_password(password)

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, role, email, department FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return User(
            user_id=row[0],
            username=row[1],
            role=row[2],
            email=row[3],
            department=row[4],
        )

    def get_all_users(self) -> List[User]:
        """Retrieve all registered users."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role, email, department FROM users")
        rows = cursor.fetchall()
        conn.close()

        return [
            User(user_id=row[0], username=row[1], role=row[2], email=row[3], department=row[4])
            for row in rows
        ]
