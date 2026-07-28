Employee Dashboard for MultiMind AI Platform.

Displays:
- Daily tasks
- Personal documents
- Leave requests
- Assigned projects
- Notifications
- AI Assistant access
"""

import streamlit as st
from typing import Dict, Any


def render_employee_dashboard(data: Dict[str, Any] = None) -> None:
    """Render the Employee Dashboard."""
    st.header("Employee Dashboard")

    if data is None:
        data = {
            "daily_tasks": 5,
            "completed_tasks": 3,
            "pending_tasks": 2,
            "documents": 12,
            "leave_requests": 2,
            "assigned_projects": 3,
            "notifications": 4,
            "today_name": "Monday, July 28, 2026",
        }

    st.subheader(f"Good day! {data.get('today_name', '')}")

    st.subheader("Daily Tasks")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", data.get("daily_tasks", 0))
    with col2:
        st.metric("Completed", data.get("completed_tasks", 0))
    with col3:
        st.metric("Pending", data.get("pending_tasks", 0))

    # Task completion progress
    total = data.get("daily_tasks", 1)
    completed = data.get("completed_tasks", 0)
    st.progress(completed / total)
    st.write(f"Task completion: {completed}/{total} ({completed/total*100:.0f}%)")

    st.subheader("My Documents")
    st.metric("Documents Available", data.get("documents", 0))

    st.subheader("Assigned Projects")
    st.metric("Active Projects", data.get("assigned_projects", 0))

    st.subheader("Notifications")
    notifications = data.get("notifications", 0)
    if notifications > 0:
        st.info(f"🔔 You have {notifications} notification(s)")
    else:
        st.success("No new notifications.")

    st.subheader("Leave Requests")
    st.metric("Leave Requests", data.get("leave_requests", 0))
