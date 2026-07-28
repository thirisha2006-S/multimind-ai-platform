Project Dashboard for MultiMind AI Platform.

Displays:
- Active projects
- Deadlines
- Team allocation
- Risks
- Progress tracking
- Client information
"""

import streamlit as st
from typing import Dict, Any


def render_project_dashboard(data: Dict[str, Any] = None) -> None:
    """Render the Project Dashboard."""
    st.header("Project Dashboard")

    if data is None:
        data = {
            "active_projects": 12,
            "completed_projects": 8,
            "delayed_projects": 2,
            "total_team_members": 45,
            "upcoming_deadlines": 5,
            "overall_progress": 72,
            "risks": ["Resource shortage in Development team", "Client feedback delays"],
            "clients": 15,
        }

    st.subheader("Project Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Active Projects", data.get("active_projects", 0))
        st.metric("Completed Projects", data.get("completed_projects", 0))

    with col2:
        st.metric("Delayed Projects", data.get("delayed_projects", 0))
        st.metric("Upcoming Deadlines", data.get("upcoming_deadlines", 0))

    with col3:
        st.metric("Team Members", data.get("total_team_members", 0))
        st.metric("Clients", data.get("clients", 0))

    st.subheader("Overall Progress")
    progress = data.get("overall_progress", 0)
    st.progress(progress / 100)
    st.write(f"**{progress}% Complete**")

    st.subheader("Project Risks")
    risks = data.get("risks", [])
    if risks:
        for risk in risks:
            st.warning(f"⚠️ {risk}")
    else:
        st.success("No active project risks.")
