"""Streamlit frontend for MultiMind AI Platform."""

import streamlit as st
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from multimind.utils.config import settings
from multimind.utils.logger import get_logger
from multimind.security.auth import Authenticator, User
from multimind.security.guardrails import Guardrails
from multimind.security.audit import AuditLogger
from multimind.agents.orchestrator import run_pipeline

logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="MultiMind AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem; font-weight: 700; color: #ffffff;
        text-align: center; padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px; margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧠 MultiMind AI Platform</div>', unsafe_allow_html=True)
st.markdown("### *The AI Operating System for Enterprises*")
st.markdown("---")

# Initialize services
authenticator = Authenticator()
audit_logger = AuditLogger()
guardrails = Guardrails()


def check_authentication() -> Optional[User]:
    if "user" not in st.session_state:
        st.session_state.user = None
    user = st.session_state.user

    if user is None:
        st.sidebar.header("🔐 Login")
        with st.sidebar.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            role = st.selectbox("🎭 Role", ["ceo", "hr", "finance", "project_manager", "employee"])
            submitted = st.form_submit_button("🚀 Sign In")

            if submitted and username and password:
                user = authenticator.register_user(
                    username=username, password=password, role=role,
                    email=f"{username}@multimind.ai", department="Engineering",
                )
                st.session_state.user = user
                audit_logger.log_login(user.user_id, success=True)
                st.rerun()

        if st.session_state.user is None:
            st.info("Please log in to access the platform.")
            st.stop()

    return user


def main():
    user = check_authentication()

    # Sidebar
    st.sidebar.markdown("---")
    st.sidebar.header(f"👤 {user.username}")
    st.sidebar.markdown(f"**Role:** `{user.role.upper()}`")
    st.sidebar.markdown(f"**Department**: {user.department or 'N/A'}")
    st.sidebar.markdown("---")

    pages = {
        "🏠 Home": "home",
        "💬 AI Assistant": "assistant",
        "📊 Dashboard": "dashboard",
        "📚 Knowledge Base": "knowledge",
        "🧠 Knowledge Genome": "genome",
        "🤖 Agent Monitor": "agents",
        "🔒 Security": "security",
        "ℹ️ About": "about",
    }

    page = st.sidebar.radio("Navigation", list(pages.keys()))
    page_key = pages[page]

    renderers = {
        "home": render_home,
        "assistant": render_ai_assistant,
        "dashboard": render_dashboard_page,
        "knowledge": render_knowledge_base,
        "genome": render_knowledge_genome,
        "agents": render_agent_monitor,
        "security": render_security_page,
        "about": render_about_page,
    }

    if page_key in renderers:
        renderers[page_key](user)


# ── HOME ──────────────────────────────────────────────────
def render_home(user: User) -> None:
    st.header(f"Welcome back, {user.username}! 👋")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🏢 Total Employees", "150", delta="+12 this month")
    with c2:
        st.metric("📊 Active Projects", "12", delta="2 delayed")
    with c3:
        st.metric("💰 Revenue", "$2.5M", delta="+15.5%")
    with c4:
        st.metric("🧠 Health Score", "87/100", delta="+3")

    st.markdown("---")
    st.subheader("🚀 Quick Actions")

    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        st.button("💬 Ask AI Assistant", use_container_width=True)
    with qc2:
        st.button("📊 View Dashboard", use_container_width=True)
    with qc3:
        st.button("📚 Browse Knowledge", use_container_width=True)
    with qc4:
        st.button("🧠 Explore Genome", use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Recent Activity")
    logs = audit_logger.get_logs(user_id=user.user_id, limit=5)
    if logs:
        for log in logs:
            st.caption(f"📌 {log['timestamp'][:19]} — _{log['action']}_ on _{log['resource']}_")
    else:
        st.info("No recent activity yet. Start by asking a question in the AI Assistant!")

    audit_logger.log(user.user_id, "page_view", "home")


# ── AI ASSISTANT ──────────────────────────────────────────
def render_ai_assistant(user: User) -> None:
    st.header("💬 AI Assistant")
    st.markdown("Ask MultiMind AI anything about your organization. Powered by **LangGraph** multi-agent orchestration.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Agent status in sidebar
    with st.sidebar:
        st.subheader("🤖 Agent Pipeline")
        agents_status = [
            "🧠 Supervisor — Active",
            "📋 Planner — Active",
            "🔍 Research — Active",
            "✅ Validator — Active",
            "⚡ Conflict Checker — Active",
            "🪞 Reflection — Active",
            "📊 Aggregator — Active",
        ]
        for agent in agents_status:
            st.markdown(agent)

        st.markdown("---")
        st.subheader("⚙️ Settings")
        web_search = st.checkbox("Enable Web Search", value=True, key="web_search")
        max_steps = st.slider("Max reasoning steps", 1, 10, 5, key="max_steps")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, key="temp")

    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📎 Sources"):
                    for s in message["sources"]:
                        st.code(s, language=None)
            if message.get("confidence"):
                st.progress(message["confidence"])
                st.caption(f"Confidence: {message['confidence']:.0%}")

    # Chat input
    if prompt := st.chat_input("Ask anything about your organization..."):
        # Guardrail checks
        checks = guardrails.run_all_checks(prompt)
        blocked = any(not c.passed and c.severity == "block" for c in checks)

        if blocked:
            st.error("⚠️ Request blocked by security guardrails.")
            for c in checks:
                if not c.passed:
                    st.write(f"- _{c.check_name}_: {c.message}")
            return

        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI response via orchestrator
        with st.chat_message("assistant"):
            with st.status("🧠 MultiMind AI is reasoning...", expanded=True):
                st.write("Running agent pipeline...")

                try:
                    result = run_pipeline(
                        query=prompt,
                        context={
                            "web_search_enabled": web_search,
                        },
                    )

                    answer = result.get("answer", "No answer generated.")
                    confidence = result.get("confidence", 0.0)
                    sources = result.get("sources", [])
                    agents_invoked = result.get("agents_invoked", 0)
                    metadata = result.get("metadata", {})

                    st.markdown(answer)

                    st.progress(confidence)
                    st.caption(f"🎯 Confidence: {confidence:.0%}")

                    if sources:
                        with st.expander("📎 Sources"):
                            for s in sources:
                                st.code(s)

                    st.caption(f"🤖 {agents_invoked} agent(s) invoked")

                    if metadata.get("reflection"):
                        st.info(f"💡 _{metadata['reflection']}_")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "confidence": confidence,
                        "sources": sources,
                        "agents_invoked": agents_invoked,
                    })

                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    logger.error(f"Pipeline error: {e}")

        audit_logger.log_query(user.user_id, prompt)


# ── DASHBOARD ──────────────────────────────────────────────
def render_dashboard_page(user: User) -> None:
    st.header("📊 Dashboard")

    if not user.can_access("dashboard"):
        st.warning("🔒 You do not have permission to view dashboards.")
        return

    from multimind.dashboards.ceo import render_ceo_dashboard
    from multimind.dashboards.hr import render_hr_dashboard
    from multimind.dashboards.finance import render_finance_dashboard
    from multimind.dashboards.project import render_project_dashboard
    from multimind.dashboards.employee import render_employee_dashboard

    role_map = {
        "ceo": ("🏢 CEO Dashboard", render_ceo_dashboard),
        "hr": ("👥 HR Dashboard", render_hr_dashboard),
        "finance": ("💰 Finance Dashboard", render_finance_dashboard),
        "project_manager": ("📋 Project Dashboard", render_project_dashboard),
        "employee": ("👤 Employee Dashboard", render_employee_dashboard),
    }

    title, renderer = role_map.get(user.role, ("📊 Dashboard", None))
    st.subheader(title)

    if renderer:
        renderer()
    else:
        st.info(f"Dashboard for role `{user.role}` is not yet configured.")

    audit_logger.log_data_access(user.user_id, "dashboard")


# ── KNOWLEDGE BASE ──────────────────────────────────────────
def render_knowledge_base(user: User) -> None:
    st.header("📚 Knowledge Base")
    st.markdown("Search, upload, and manage the organization's knowledge.")

    search_tab, upload_tab, stats_tab = st.tabs(["🔍 Search", "📤 Upload", "📊 Stats"])

    with search_tab:
        query = st.text_input("Search documents...", key="kb_search", placeholder="What is our leave policy?")
        if query:
            st.info(f"Searching for: _{query}_")
            st.write("Results would appear here with source references and confidence scores.")

    with upload_tab:
        uploaded = st.file_uploader(
            "Upload documents", type=["pdf", "docx", "xlsx", "txt", "md"],
            accept_multiple_files=True, key="kb_upload",
        )
        if uploaded:
            for f in uploaded:
                st.write(f"📄 {f.name} ({(f.size / 1024):.1f} KB)")
            st.success(f"✅ {len(uploaded)} file(s) ready for ingestion into FAISS vector store.")

    with stats_tab:
        st.metric("Total Documents", "0 (development mode)")
        st.metric("Total Chunks (FAISS)", "0")
        st.metric("Last Indexed", "N/A")


# ── KNOWLEDGE GENOME ────────────────────────────────────────
def render_knowledge_genome(user: User) -> None:
    st.header("🧠 Knowledge Genome")
    st.markdown("Explore your company's unique organizational patterns and intelligence.")

    st.info(
        "The Knowledge Genome learns how your company operates — decision patterns, "
        "approval workflows, team collaboration styles, business strategies — "
        "creating organization-specific intelligence beyond generic AI knowledge."
    )

    from multimind.memory.genome import KnowledgeGenome
    genome = KnowledgeGenome()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Genome Health")
        report = genome.get_health_report()
        st.metric("Total Patterns", report.get("total_patterns", 0))
        st.metric("Overall Confidence", f"{report.get('overall_confidence', 0):.1%}")
        for ptype, count in report.get("pattern_types", {}).items():
            st.write(f"- _{ptype}_: **{count}** patterns")

    with col2:
        st.subheader("🎯 Pattern Types")
        st.markdown("""
        - **Decision Patterns** — How the company makes decisions
        - **Approval Workflows** — Standard approval chains
        - **Team Collaboration** — Working styles across teams
        - **Project Outcomes** — Success and failure patterns
        - **Customer Behavior** — Customer interaction patterns
        - **Risk Profiles** — Organizational risk tolerance
        """)


# ── AGENT MONITOR ───────────────────────────────────────────
def render_agent_monitor(user: User) -> None:
    st.header("🤖 Agent Monitor")
    st.markdown("Real-time status and activity of all MultiMind AI agents.")

    agents = [
        ("Supervisor Agent", "🧠", "Controls workflow and delegates tasks", "🟢 Active"),
        ("Planner Agent", "📋", "Decomposes complex tasks into steps", "🟢 Active"),
        ("Research Agent", "🔍", "Searches internal docs + web sources", "🟢 Active"),
        ("Validator Agent", "✅", "Verifies answer correctness", "🟢 Active"),
        ("Conflict Detection", "⚡", "Detects contradictory information", "🟠 Standing By"),
        ("Reflection Agent", "🪞", "Learns from past executions", "🟢 Active"),
        ("Finance AI", "💰", "Financial analysis specialist", "🟢 Active"),
        ("HR AI", "👥", "HR management specialist", "🟢 Active"),
        ("Legal AI", "⚖️", "Legal and compliance specialist", "🟢 Active"),
        ("Project AI", "📋", "Project management specialist", "🟢 Active"),
        ("Sales AI", "📈", "Sales and CRM specialist", "🟢 Active"),
        ("Security AI", "🔒", "Security monitoring specialist", "🟢 Active"),
    ]

    for name, icon, desc, status in agents:
        st.markdown(f"**{icon} {name}** — _{desc}_ — {status}")

    st.markdown("---")
    st.subheader("📊 Agent Execution History")

    history = [
        {"time": "2 min ago", "query": "What is our revenue trend?", "agents": "5", "status": "✅ Success"},
        {"time": "5 min ago", "query": "Which projects are at risk?", "agents": "4", "status": "✅ Success"},
        {"time": "12 min ago", "query": "Leave policy for Q4", "agents": "3", "status": "✅ Success"},
        {"time": "18 min ago", "query": "Budget analysis for marketing", "agents": "6", "status": "⚠️ Review Needed"},
    ]

    for h in history:
        st.write(f"**{h['time']}** — _{h['query']}_ — {h['agents']} agents — {h['status']}")


# ── SECURITY ────────────────────────────────────────────────
def render_security_page(user: User) -> None:
    st.header("🔒 Security")

    if user.role != "ceo":
        st.warning("🔒 Security settings are restricted to CEO access.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ Guardrail Status")
        st.success("✅ Prompt Injection Detection: **Active**")
        st.success("✅ SQL Injection Prevention: **Active**")
        st.success("✅ PII Masking: **Active**")
        st.success("✅ Audit Logging: **Active**")
        st.success("✅ Multi-Tenant Data Isolation: **Active**")
        st.success("✅ Role-Based Access Control (RBAC): **Active**")

    with col2:
        st.subheader("📋 Audit Log (Last 10)")
        logs = audit_logger.get_logs(limit=10)
        if logs:
            for log in logs[:5]:
                st.caption(f"{log['timestamp'][:19]} — _{log['action']}_ → _{log['resource']}_")
        else:
            st.write("No audit entries yet.")

    st.markdown("---")
    st.subheader("Human Approval Workflow")
    st.info("Critical operations route through human-in-the-loop approval before execution.")


# ── ABOUT ────────────────────────────────────────────────────
def render_about_page(user: User) -> None:
    st.header("ℹ️ About MultiMind AI")

    st.markdown("""
    ### 🧠 MultiMind AI Platform
    **The AI Operating System for Enterprises**

    MultiMind AI unifies organizational knowledge, documents, projects, employees, and business
    intelligence into one secure, multi-agent platform with explainable AI, organizational memory,
    and decision support.
    """)

    st.markdown("---")
    st.subheader("Key Features")
    features = [
        "Multi-Agent AI Architecture (Supervisor, Planner, Research, Validator, Conflict Detection, Reflection)",
        "Company Knowledge Genome (organization-specific intelligence)",
        "Enterprise Digital Twin (relationship mapping)",
        "Organizational Memory (preserves knowledge when employees leave)",
        "Future Business Simulator (what-if scenario modeling)",
        "AI Executive Council (specialized agents collaborate before final answers)",
        "Company Health Engine (live health scoring across 7 dimensions)",
        "Silent AI (proactive problem detection)",
        "Knowledge Doctor (automatic knowledge base maintenance)",
        "Explainable AI (full transparency into every answer)",
        "Agent Replay (debug and audit any AI workflow)",
    ]
    for f in features:
        st.write(f"- {f}")

    st.markdown("---")
    st.subheader("Technology Stack")
    tech = [
        ("Frontend", "Streamlit"),
        ("Backend", "Python"),
        ("AI Framework", "LangChain + LangGraph"),
        ("AI Models", "Cohere API + OpenAI API"),
        ("Web Search", "Tavily Search API"),
        ("Database", "SQLite"),
        ("Vector DB", "FAISS"),
        ("Deployment", "Docker + AWS"),
    ]
    for label, tech_name in tech:
        st.write(f"- **{label}:** _{tech_name}_")

    st.markdown("---")
    st.caption("Version 0.1.0 | © 2026 MultiMind AI | thirishasriram079@gmail.com")

    audit_logger.log(user.user_id, "page_view", "about")


if __name__ == "__main__":
    main()
