Dashboard data module for MultiMind AI Platform.

Provides get_dashboard_data() which returns role-specific KPI cards
and notes for each dashboard view.
"""


def get_dashboard_data(role: str) -> dict:
    """Return role-specific dashboard data."""
    dashboards = {
        "ceo": {
            "kpis": [
                ("Total Employees", "150"),
                ("Active Projects", "12"),
                ("Revenue", "$2.5M"),
                ("Company Health", "87/100"),
            ],
            "tones": ["good", "good", "good", "good"],
            "note": "CEO overview showing company-wide metrics. Connect HRIS and financial systems for live data.",
        },
        "hr": {
            "kpis": [
                ("Total Employees", "150"),
                ("Open Positions", "8"),
                ("Attendance", "94.5%"),
                ("Avg Performance", "4.2/5"),
            ],
            "tones": ["good", "warn", "good", "good"],
            "note": "HR metrics for recruitment, attendance, and performance tracking.",
        },
        "finance": {
            "kpis": [
                ("Revenue", "$2.5M"),
                ("Expenses", "$1.8M"),
                ("Cash Flow", "$320K"),
                ("Profit Margin", "28%"),
            ],
            "tones": ["good", "warn", "good", "good"],
            "note": "Financial overview. Connect accounting system for real-time figures.",
        },
        "project_manager": {
            "kpis": [
                ("Active Projects", "12"),
                ("Delayed", "2"),
                ("Team Size", "45"),
                ("On Track", "72%"),
            ],
            "tones": ["good", "bad", "good", "warn"],
            "note": "Project status with deadline and resource tracking.",
        },
        "employee": {
            "kpis": [
                ("My Tasks", "5"),
                ("Completed", "3"),
                ("Documents", "12"),
                ("Projects", "3"),
            ],
            "tones": ["neutral", "good", "good", "good"],
            "note": "Personal view of assigned tasks and documents.",
        },
    }

    return dashboards.get(role, dashboards["employee"])
