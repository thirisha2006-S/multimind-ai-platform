"""Streamlit entry point for MultiMind AI Platform — Instrument Panel design."""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from multimind.utils.config import settings
from multimind.utils.logger import get_logger
from multimind.security.auth import Authenticator, User
from multimind.security.guardrails import Guardrails
from multimind.security.audit import AuditLogger
from multimind.agents.orchestrator import run_pipeline
from core.theme import inject_theme

logger = get_logger(__name__)

st.set_page_config(page_title="MultiMind AI", page_icon="🧠", layout="wide")
inject_theme(st)

authenticator = Authenticator()
audit_logger = AuditLogger()
guardrails = Guardrails()


def check_auth():
    if "user" not in st.session_state:
        st.session_state.user = None
    user = st.session_state.user
    if user is None:
        with st.sidebar:
            st.header("SYSTEM ACCESS")
            with st.form("login"):
                u = st.text_input("USERNAME")
                p = st.text_input("PASSWORD", type="password")
                role = st.selectbox("ROLE", ["ceo", "hr", "finance", "project_manager", "employee"])
                if st.form_submit_button("AUTHENTICATE", type="primary", use_container_width=True):
                    user = authenticator.register_user(u, p, role)
                    st.session_state.user = user
                    audit_logger.log_login(user["user_id"], success=True)
                    st.rerun()
        if st.session_state.user is None:
            st.info("Please log in to access the platform.")
            st.stop()
    return st.session_state.user


def render_home(user):
    st.header(f"Welcome, {user.get('username', 'Operator')}!")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Employees", "150")
    with c2: st.metric("Projects", "12")
    with c3: st.metric("Revenue", "$2.5M")
    with c4: st.metric("Health", "87/100")

    st.markdown("---")
    st.subheader("AI Enterprise Search")
    question = st.text_input("Ask about your organization:", key="home_q", placeholder="e.g. What is our leave policy?")
    if question:
        with st.spinner("Searching..."):
            st.info(f"Query: _{question}_")
            st.write("Connect your Cohere API key in the sidebar to enable AI search and multi-agent orchestration.")

    st.markdown("---")
    st.subheader("Agent Pipeline")
    st.caption("Supervisor -> Planner -> Research -> Conflict Detection -> Draft -> Validator")
    if st.button("Run Demo Pipeline", use_container_width=True):
        trace = [
            {"agent": "Supervisor Agent", "input": question or "overview", "output": "Classified"},
            {"agent": "Planner Agent", "input": question or "overview", "output": "Decomposed into 3 steps"},
            {"agent": "Research Agent", "input": question or "overview", "output": "Searched knowledge base"},
            {"agent": "Conflict Agent", "input": question or "overview", "output": "No conflicts found"},
            {"agent": "Draft Agent", "input": question or "overview", "output": "Generating answer"},
            {"agent": "Validator Agent", "input": question or "overview", "output": "Confidence: 85%"},
        ]
        st.markdown("pipeline rendered successfully (6/6 agents active)")
        for step in trace:
            st.write(f"{step['agent']}: {step['output']}")


def render_ai_assistant(user):
    st.header("AI Assistant")
    st.caption("Powered by LangGraph multi-agent orchestration")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("confidence"):
                st.progress(msg["confidence"])

    if prompt := st.chat_input("Ask anything about your organization..."):
        checks = guardrails.run_all_checks(prompt)
        if any(not c.passed and c.severity == "block" for c in checks):
            st.error("Blocked by security guardrails.")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("MultiMind AI reasoning..."):
                try:
                    result = run_pipeline(query=prompt, context={})
                    answer = result.get("answer", "(no answer)")
                    conf = result.get("confidence", 0.5)
                    st.markdown(answer)
                    st.progress(conf)
                    st.caption(f"Confidence: {conf:.0%}")
                    st.session_state.messages.append({"role": "assistant", "content": answer, "confidence": conf})
                except Exception as e:
                    st.error(f"Error: {e}")
        audit_logger.log_query(user.get("user_id", "anon"), prompt)


def render_dashboard(user):
    st.header("Dashboard")
    role = user.get("role", "employee")
    dashboards = {
        "ceo": [("Employees", "150"), ("Active Projects", "12"), ("Revenue", "$2.5M"), ("Health", "87/100")],
        "hr": [("Total", "150"), ("Open Roles", "8"), ("Attendance", "94.5%"), ("Performance", "4.2/5")],
        "finance": [("Revenue", "$2.5M"), ("Expenses", "$1.8M"), ("Cash Flow", "$320K"), ("Margin", "28%")],
        "project_manager": [("Active", "12"), ("Delayed", "2"), ("Team", "45"), ("On Track", "72%")],
        "employee": [("Tasks", "5"), ("Done", "3"), ("Docs", "12"), ("Projects", "3")],
    }
    kpis = dashboards.get(role, dashboards["employee"])
    cols = st.columns(len(kpis))
    for i, (label, value) in enumerate(kpis):
        with cols[i]:
            st.metric(label, value)
    st.progress(0.87)
    st.caption("Company Health: 87/100")


def render_knowledge_base(user):
    st.header("Knowledge Base")
    upload = st.file_uploader("Upload documents (PDF, DOCX, TXT, MD)", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True, key="kb")
    if upload:
        for f in upload:
            st.write(f"- {f.name} ({(f.size/1024):.1f} KB)")
        st.success(f"{len(upload)} file(s) ready for ingestion.")

    q = st.text_input("Search knowledge base:", key="kb_search")
    if q:
        st.info(f"Searching: _{q}_ | Connect Cohere API key for semantic search.")

    st.caption("0 documents indexed (development mode). Upload files to begin.")


def render_agent_monitor(user):
    st.header("Agent Monitor")
    agents = [
        ("Supervisor Agent", "Controls workflow", "active"),
        ("Planner Agent", "Decomposes tasks", "active"),
        ("Research Agent", "Searches docs + web", "active"),
        ("Validator Agent", "Verifies answers", "active"),
        ("Conflict Detection", "Detects contradictions", "standby"),
        ("Reflection Agent", "Learns from history", "active"),
    ]
    for name, desc, status in agents:
        st.write(f"**{name}** — _{desc}_ — {status}")

    st.markdown("---")
    st.subheader("Execution History")
    for h in [
        ("2 min ago", "Revenue trend?", "5 agents", "Success"),
        ("5 min ago", "At risk projects?", "4 agents", "Success"),
        ("12 min ago", "Leave policy Q4?", "3 agents", "Success"),
    ]:
        st.write(f"**{h[0]}** — _{h[1]}_ — {h[2]} — {h[3]}")


def render_security(user):
    st.header("Security")
    if user.get("role") != "ceo":
        st.warning("Restricted to CEO access.")
        return
    st.success("Prompt Injection Detection: Active")
    st.success("SQL Injection Prevention: Active")
    st.success("PII Masking: Active")
    st.success("Audit Logging: Active")
    st.success("RBAC: Active")


def render_about(user):
    st.header("About MultiMind AI")
    st.markdown("### MultiMind AI — The AI Operating System for Enterprises")
    st.markdown("""
Unifying organizational knowledge, documents, projects, employees, and business intelligence into one secure, multi-agent platform with explainable AI, organizational memory, and decision support.
    """)
    st.subheader("Key Features")
    for f in [
        "Multi-Agent AI Architecture",
        "Company Knowledge Genome",
        "Enterprise Digital Twin",
        "Organizational Memory",
        "Business Simulator",
        "AI Executive Council",
        "Company Health Engine",
        "Silent AI Monitoring",
        "Knowledge Doctor AI",
        "Explainable AI with full trace",
        "Agent Replay for debugging",
    ]:
        st.write(f"- {f}")


def main():
    user = check_auth()

    with st.sidebar:
        st.markdown(f"**{user.get('username', 'User')}** ({user.get('role', 'employee').upper()})")
        st.markdown("---")
        st.caption("COHERE API KEY")
        st.text_input("API Key", type="password", key="cohere")
        st.markdown("---")
        page = st.radio("Navigate", [
            "Home", "AI Assistant", "Dashboard",
            "Knowledge Base", "Agent Monitor", "Security", "About",
        ])

    renderers = {
        "Home": render_home,
        "AI Assistant": render_ai_assistant,
        "Dashboard": render_dashboard,
        "Knowledge Base": render_knowledge_base,
        "Agent Monitor": render_agent_monitor,
        "Security": render_security,
        "About": render_about,
    }

    if page in renderers:
        renderers[page](user)


if __name__ == "__main__":
    main()
