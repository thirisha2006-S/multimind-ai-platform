"""MultiMind AI — Instrument Panel frontend entry point."""

import streamlit as st
import sys
import os

# Ensure src and core are on the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multimind.utils.config import settings
from multimind.utils.logger import get_logger
from multimind.security.auth import Authenticator, User
from multimind.security.guardrails import Guardrails
from multimind.security.audit import AuditLogger
from multimind.agents.orchestrator import run_pipeline, build_orchestrator
from core.theme import inject_theme, topbar_html, kpi_cards_html, health_bar_html, pipeline_html, trace_step_html

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
            st.header("🔐 Login")
            with st.form("login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["ceo", "hr", "finance", "project_manager", "employee"])
                if st.form_submit_button("Sign In", use_container_width=True):
                    user = authenticator.register_user(u, p, role)
                    st.session_state.user = user
                    audit_logger.log_login(user["user_id"], success=True)
                    st.rerun()
        if st.session_state.user is None:
            st.info("Please log in to continue.")
            st.stop()
    return st.session_state.user


def render_home(user):
    st.header(f"Welcome, {user.get('username', 'Admin')}! 👋")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Employees", "150", "+12")
    with c2: st.metric("Projects", "12", "2 delayed")
    with c3: st.metric("Revenue", "$2.5M", "+15.5%")
    with c4: st.metric("Health", "87/100", "+3")

    st.markdown("---")
    st.subheader("🔍 AI Enterprise Search")
    question = st.text_input("Ask about your organization:", key="home_search", placeholder="e.g. What is our leave policy?")
    if question:
        with st.spinner("Searching..."):
            kb = None  # placeholder — would connect to KnowledgeBase in production
            st.info(f"Query: _{question}_")
            st.write("Connect your Cohere API key in the sidebar to enable search.")

    st.markdown("---")
    st.subheader("🤖 Multi-Agent Pipeline")
    st.caption("Supervisor → Planner → Research → Conflict Detection → Draft → Validator")
    if st.button("Run Demo Pipeline", use_container_width=True):
        placeholder = st.empty()
        trace = [
            {"agent": "Supervisor Agent", "input": question or "company overview", "output": "Classified query type"},
            {"agent": "Planner Agent", "input": question or "company overview", "output": "Decomposed into 3 sub-questions"},
            {"agent": "Research Agent", "input": question or "company overview", "output": "Searched internal knowledge base"},
            {"agent": "Conflict Agent", "input": question or "company overview", "output": "No conflicts found"},
            {"agent": "Draft Agent", "input": question or "company overview", "output": "Generating comprehensive answer"},
            {"agent": "Validator Agent", "input": question or "company overview", "output": "Confidence: 85% - validated"},
        ]
        placeholder.markdown(pipeline_html(trace), unsafe_allow_html=True)
        placeholder.markdown("**Answer:** MultiMind AI is your enterprise AI Operating System — unifying knowledge, documents, and decision-making into one secure platform.", unsafe_allow_html=False)
        st.caption("Agent Pipeline complete — all 6 agents executed successfully.")


def render_ai_assistant(user):
    st.header("💬 AI Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("confidence"):
                st.progress(msg["confidence"])

    if prompt := st.chat_input("Ask anything..."):
        checks = guardrails.run_all_checks(prompt)
        if any(not c.passed and c.severity == "block" for c in checks):
            st.error("Blocked by security guardrails.")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Running agent pipeline..."):
                try:
                    result = run_pipeline(query=prompt, context={})
                    st.markdown(result.get("answer", "No answer."))
                    conf = result.get("confidence", 0.5)
                    st.progress(conf)
                    st.caption(f"Confidence: {conf:.0%} | Agents: {result.get('agents_invoked', 0)}")
                    st.session_state.messages.append({"role": "assistant", "content": result.get("answer", ""), "confidence": conf})
                except Exception as e:
                    st.error(f"Error: {e}")

        audit_logger.log_query(user.get("user_id", "anon"), prompt)


def render_dashboard(user):
    st.header("📊 Dashboard")
    role = user.get("role", "employee")
    dashboards = {
        "ceo": {"title": "CEO Dashboard", "kpis": [("Employees", "150"), ("Projects", "12"), ("Revenue", "$2.5M"), ("Health", "87/100")], "tones": ["good", "good", "good", "good"]},
        "hr": {"title": "HR Dashboard", "kpis": [("Employees", "150"), ("Open Roles", "8"), ("Attendance", "94.5%"), ("Performance", "4.2/5")], "tones": ["good", "warn", "good", "good"]},
        "finance": {"title": "Finance Dashboard", "kpis": [("Revenue", "$2.5M"), ("Expenses", "$1.8M"), ("Cash Flow", "$320K"), ("Margin", "28%")], "tones": ["good", "warn", "good", "good"]},
        "project_manager": {"title": "Project Dashboard", "kpis": [("Active", "12"), ("Delayed", "2"), ("Team", "45"), ("On Track", "72%")], "tones": ["good", "bad", "good", "warn"]},
        "employee": {"title": "Employee Dashboard", "kpis": [("Tasks", "5"), ("Done", "3"), ("Docs", "12"), ("Projects", "3")], "tones": ["neutral", "good", "good", "good"]},
    }
    d = dashboards.get(role, dashboards["employee"])
    st.subheader(d["title"])
    st.markdown(kpi_cards_html(list(zip(d["kpis"][::2], d["kpis"][1::2])), d["tones"]), unsafe_allow_html=True)

    # Health score
    st.markdown("---")
    st.subheader("🏥 Company Health")
    st.markdown(health_bar_html(87), unsafe_allow_html=True)
    st.caption("Overall Health Score: 87/100 (improving)")


def render_knowledge_base(user):
    st.header("📚 Knowledge Base")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Search")
        q = st.text_input("Search documents:", key="kb_search")
        if q:
            st.info(f"Searching for: _{q}_")
            st.write("Connect Cohere API key in sidebar to enable search.")
    with col2:
        st.subheader("Upload")
        files = st.file_uploader("Upload documents", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True, key="kb_upload")
        if files:
            for f in files:
                st.write(f"📄 {f.name} ({(f.size / 1024):.1f} KB)")
            st.success(f"{len(files)} file(s) ready for ingestion.")

    st.markdown("---")
    st.subheader("Indexed Documents")
    st.caption("0 documents indexed (development mode). Upload files to begin indexing.")


def render_agent_monitor(user):
    st.header("🤖 Agent Monitor")
    agents = [
        ("Supervisor Agent", "Controls workflow", "🟢 Active"),
        ("Planner Agent", "Decomposes tasks", "🟢 Active"),
        ("Research Agent", "Searches docs + web", "🟢 Active"),
        ("Validator Agent", "Verifies answers", "🟢 Active"),
        ("Conflict Detection", "Detects contradictions", "🟠 Standby"),
        ("Reflection Agent", "Learns from history", "🟢 Active"),
    ]
    for name, desc, status in agents:
        st.markdown(f"**{name}** — _{desc}_ {status}")

    st.markdown("---")
    st.subheader("Execution History")
    history = [
        {"time": "2 min ago", "query": "Revenue trend", "agents": "5", "status": "✅ Success"},
        {"time": "5 min ago", "query": "At risk projects", "agents": "4", "status": "✅ Success"},
        {"time": "12 min ago", "query": "Leave policy Q4", "agents": "3", "status": "✅ Success"},
    ]
    for h in history:
        st.write(f"**{h['time']}** — _{h['query']}_ — {h['agents']} agents — {h['status']}")


def render_security(user):
    st.header("🔒 Security")
    if user.get("role") != "ceo":
        st.warning("Restricted to CEO access.")
        return
    st.success("✅ Prompt Injection Detection: Active")
    st.success("✅ SQL Injection Prevention: Active")
    st.success("✅ PII Masking: Active")
    st.success("✅ Audit Logging: Active")
    st.success("✅ RBAC: Active")
    logs = audit_logger.get_logs(limit=5)
    if logs:
        for log in logs[:3]:
            st.caption(f"{log['timestamp'][:19]} — _{log['action']}_ → _{log['resource']}_")


def render_about(user):
    st.header("ℹ️ About MultiMind AI")
    st.markdown("""
    ### MultiMind AI — The AI Operating System for Enterprises
    **Unifying organizational knowledge, documents, projects, employees,
    and business intelligence into one secure, multi-agent platform.**
    """)
    st.subheader("Key Features")
    for feat in [
        "Multi-Agent AI Architecture",
        "Company Knowledge Genome",
        "Enterprise Digital Twin",
        "Organizational Memory",
        "Future Business Simulator",
        "AI Executive Council",
        "Company Health Engine",
        "Silent AI — Proactive monitoring",
        "Knowledge Doctor AI",
        "Explainable AI with full trace",
        "Agent Replay for debugging",
    ]:
        st.write(f"- {feat}")
    st.markdown("---")
    st.caption("v0.1.0 | © 2026 MultiMind AI | thirishasriram079@gmail.com")


def main():
    user = check_auth()

    with st.sidebar:
        st.markdown(f"**👤 {user.get('username', 'User')}**")
        st.caption(f"Role: `{user.get('role', 'employee').upper()}`")
        st.markdown("---")
        st.caption("Enter Cohere API key to enable AI features:")
        api_key = st.text_input("COHERE API KEY", type="password", key="cohere_key")
        if api_key:
            os.environ["COHERE_API_KEY"] = api_key
        st.markdown("---")

        page = st.radio("Navigate", [
            "🏠 Home", "💬 AI Assistant", "📊 Dashboard",
            "📚 Knowledge Base", "🤖 Agent Monitor",
            "🔒 Security", "ℹ️ About",
        ])

    # Map pages to renderers
    pages = {
        "🏠 Home": render_home,
        "💬 AI Assistant": render_ai_assistant,
        "📊 Dashboard": render_dashboard,
        "📚 Knowledge Base": render_knowledge_base,
        "🤖 Agent Monitor": render_agent_monitor,
        "🔒 Security": render_security,
        "ℹ️ About": render_about,
    }

    if page in pages:
        pages[page](user)


if __name__ == "__main__":
    main()
