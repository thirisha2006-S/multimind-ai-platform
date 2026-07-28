Finance Dashboard for MultiMind AI Platform.

Displays:
- Revenue and expenses
- Budget tracking
- Payroll costs
- Invoices
- Cash flow
"""

import streamlit as st
from typing import Dict, Any


def render_finance_dashboard(data: Dict[str, Any] = None) -> None:
    """Render the Finance Dashboard."""
    st.header("Finance Dashboard")

    if data is None:
        data = {
            "revenue": 2500000,
            "expenses": 1800000,
            "budget": 2000000,
            "payroll": 750000,
            "invoices_pending": 15,
            "invoices_paid": 120,
            "cash_flow": 320000,
            "profit_margin": 28.0,
            "budget_utilization": 90.0,
        }

    st.subheader("Financial Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Revenue", f"${data.get('revenue', 0):,.0f}")
        st.metric("Expenses", f"${data.get('expenses', 0):,.0f}")

    with col2:
        st.metric("Budget", f"${data.get('budget', 0):,.0f}")
        st.metric("Budget Utilization", f"{data.get('budget_utilization', 0)}%")
        st.progress(data.get("budget_utilization", 0) / 100)

    with col3:
        st.metric("Payroll", f"${data.get('payroll', 0):,.0f}")
        st.metric("Cash Flow", f"${data.get('cash_flow', 0):,.0f}")

    st.subheader("Invoices")
    col_inv1, col_inv2 = st.columns(2)
    with col_inv1:
        st.metric("Pending Invoices", data.get("invoices_pending", 0))
    with col_inv2:
        st.metric("Paid Invoices", data.get("invoices_paid", 0))

    st.subheader("Profit Margin")
    profit_margin = data.get("profit_margin", 0)
    st.metric("Profit Margin", f"{profit_margin}%")
    st.progress(profit_margin / 100)
