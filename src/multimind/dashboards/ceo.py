CEO Dashboard for MultiMind AI Platform.

Displays:
- Total Employees
- Total Departments
- Active Projects
- Delayed Projects
- Clients
- Revenue
- Profit
- Cash Flow
- Business Growth
- AI Predictions
- Company Health Score
- Risk Analysis
"""

import streamlit as st
from typing import Dict, Any


def render_ceo_dashboard(data: Dict[str, Any] = None) -> None:
    """Render the CEO Dashboard."""
    st.header("CEO Dashboard")

    # Default sample data
    if data is None:
        data = {
            "total_employees": 150,
            "total_departments": 8,
            "active_projects": 12,
            "delayed_projects": 2,
            "clients": 45,
            "revenue": 2500000,
            "profit": 450000,
            "cash_flow": 320000,
            "growth_rate": 15.5,
            "health_score": 87,
            "risks": ["Market competition", "Resource constraints"],
            "ai_predictions": [
                "Revenue expected to grow 12% next quarter",
                "Hiring shortage projected in Q3",
            ],
        }

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Employees", data.get("total_employees", 0))
        st.metric("Total Departments", data.get("total_departments", 0))

    with col2:
        st.metric("Active Projects", data.get("active_projects", 0))
        st.metric("Delayed Projects", data.get("delayed_projects", 0))

    with col3:
        st.metric("Clients", data.get("clients", 0))
        st.metric("Revenue", f"${data.get('revenue', 0):,.0f}")

    with col4:
        st.metric("Profit", f"${data.get('profit', 0):,.0f}")
        st.metric("Cash Flow", f"${data.get('cash_flow', 0):,.0f}")

    st.subheader("Business Growth")
    st.metric("Growth Rate", f"{data.get('growth_rate', 0)}%", delta=f"{data.get('growth_rate', 0)}%")

    st.subheader("Company Health Score")
    health_score = data.get("health_score", 0)
    st.progress(health_score / 100)
    st.write(f"**Health Score: {health_score}/100**")

    st.subheader("Risk Analysis")
    risks = data.get("risks", [])
    if risks:
        for risk in risks:
            st.warning(f"⚠️ {risk}")
    else:
        st.success("No significant risks detected.")

    st.subheader("AI Predictions")
    predictions = data.get("ai_predictions", [])
    if predictions:
        for pred in predictions:
            st.info(f"🔮 {pred}")
    else:
        st.info("No predictions available yet.")
