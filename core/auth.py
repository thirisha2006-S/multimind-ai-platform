"""Authentication module for MultiMind AI Platform."""
Provides demo credentials and a simple authenticate function.
"""

ROLES = ["ceo", "hr", "finance", "project_manager", "employee"]

DEMO_CREDENTIALS = {
    "ceo": {"password": "ceo123", "display_name": "Chief Executive Officer"},
    "hr": {"password": "hr123", "display_name": "HR Manager"},
    "finance": {"password": "finance123", "display_name": "Finance Director"},
    "project_manager": {"password": "pm123", "display_name": "Project Manager"},
    "employee": {"password": "emp123", "display_name": "Team Member"},
}


def authenticate(username: str, password: str):
    """Authenticate a user. Returns a user dict or None."""
    for role, creds in DEMO_CREDENTIALS.items():
        if username == role and password == creds["password"]:
            return {
                "role": role,
                "username": username,
                "display_name": creds["display_name"],
                "department": role.capitalize(),
            }
    return None


def demo_credentials_hint() -> str:
    """Return a formatted string showing all demo credentials."""
    lines = ["| Role | Username | Password |"]
    lines.append("|------|----------|----------|")
    for role, creds in DEMO_CREDENTIALS.items():
        lines.append(f"| {role} | {role} | {creds['password']} |")
    return "\n".join(lines)
