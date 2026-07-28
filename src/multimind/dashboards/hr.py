HR Dashboard for MultiMind AI Platform.

Displays:
- Employee count and stats
- Recruitment pipeline
- Attendance tracking
- Leave management
- Performance metrics
- Training progress
- Promotions tracking
"""

import streamlit as st
from typing import Dict, Any


def render_hr_dashboard(data: Dict[str, Any] = None) -> None:
    """Render the HR Dashboard."""
    st.header("HR Dashboard")

    if data is None:
        data = {
            "total_employees": 150,
            "new_hires": 12,
            "open_positions": 8,
            "attendance_rate": 94.5,
            "leave_requests": 23,
            "approved_leaves": 20,
            "pending_leaves": 3,
            "avg_performance": 4.2,
            "training_completed": 67,
            "training_pending": 15,
            "promotions": 5,
        }

    st.subheader("Employee Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Employees", data.get("total_employees", 0))
        st.metric("New Hires (This Month)", data.get("new_hires", 0))

    with col2:
        st.metric("Open Positions", data.get("open_positions", 0))
        st.metric("Attendance Rate", f"{data.get('attendance_rate', 0)}%")

    with col3:
        leave_data = data.get("leave_requests", 0)
        st.metric("Leave Requests", leave_data)
        st.metric("Approved", data.get("approved_leaves", 0))
        st.metric("Pending", data.get("pending_leaves", 0))

    with col4:
        st.metric("Avg Performance Score", data.get("avg_performance", 0))
        st.metric("Promotions This Quarter", data.get("promotions", 0))

    st.subheader("Training Progress")
    completed = data.get("training_completed", 0)
    pending = data.get("training_pending", 0)
    st.metric("Completed", completed)
    st.metric("Pending", pending)

    # Training progress bar
    total_training = completed + pending
    if total_training > 0:
        st.progress(completed / total_training)
        st.write(f"Training completion: {completed}/{total_training} ({completed/total_training*100:.1f}%)")
