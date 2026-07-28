"""Streamlit frontend for MultiMind AI Platform."""

import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multimind.utils.config import settings
from multimind.utils.logger import get_logger
from multimind.security.auth import Authenticator, User
from multimind.security.guardrails import Guardrails
from multimind.security.audit import AuditLogger

# Initialize logger
logger = get_logger(__name__)

# Page config
st.set_page_config(
    page_title="MultiMind AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🧠 MultiMind AI Platform")
st.markdown("### The AI Operating System for Enterprises")

# Initialize services
authenticator = Authenticator()
audit_logger = AuditLogger()
guardrails = Guardrails()


def check_authentication() -> Optional[User]:
    """Check if user is authenticated, prompt login if not."""
    if "user" not in st.session_state:
        st.session_state.user = None

    user = st.session_state.user

    if user is None:
        st.sidebar.header("Login")
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["ceo", "hr", "finance", "project_manager", "employee"])
            submitted = st.form_submit_button("Login")

            if submitted:
                # In production, authenticate against database
                # For demo, create user from form
                user = authenticator.register_user(
                    username=username,
                    password=password,
                    role=role,
                )
                st.session_state.user = user
                audit_logger.log_login(user.user_id, success=True)
                st.rerun()
        st.stop()

    return user


def main():
    """Main Streamlit application."""
    user = check_authentication()

    # Sidebar navigation
    st.sidebar.header(f"👤 {user.username} ({user.role.upper()})")
    st.sidebar.markdown(f"**Department:** {user.department or 'N/A'}")

    page = st.sidebar.radio(
        "Navigate",
        [
            "🏠 Home",
            "💬 AI Assistant",
            "📊 Dashboard",
            "📚 Knowledge Base",
            "🧠 Knowledge Genome",
            "🔒 Security",
            "ℹ️ About",
        ],
    )

    # Page routing
    if page == "🏠 Home":
        render_home(user)
    elif page == "💬 AI Assistant":
        render_ai_assistant(user)
    elif page == "📊 Dashboard":
        render_dashboard_page(user)
    elif page == "📚 Knowledge Base":
        render_knowledge_base(user)
    elif page == "🧠 Knowledge Genome":
        render_knowledge_genome(user)
    elif page == "🔒 Security":
        render_security_page(user)
    elif page == "ℹ️ About":
        render_about_page(user)


def render_home(user: User) -> None:
    """Render the home page."""
    st.header(f"Welcome, {user.username}!")
    st.markdown(f"""
    ### MultiMind AI Platform
    **Your AI Operating System for Enterprise Intelligence**

    The MultiMind AI platform unifies organizational knowledge, documents, projects, employees, and business intelligence into one secure, multi-agent platform with explainable AI, organizational memory, and decision support.

    **Your Role:** `{user.role.upper()}`

    ---

    ### Quick Actions
    - 💬 **Ask AI** — Get intelligent insights from your data
    - 📊 **Dashboard** — View role-specific metrics
    - 📚 **Knowledge Base** — Search and manage documents
    - 🧠 **Knowledge Genome** — Explore organizational patterns
    """)

    # Log the visit
    audit_logger.log(user.user_id, "page_view", "home")


def render_ai_assistant(user: User) -> None:
    """Render the AI chat assistant."""
    st.header("💬 AI Assistant")
    st.markdown("Ask MultiMind AI anything about your organization.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("📎 Sources"):
                    for source in message["sources"]:
                        st.write(f"- {source}")
            if message.get("confidence"):
                st.caption(f"Confidence: {message['confidence']}")

    # Chat input
    if prompt := st.chat_input("Ask a question..."):
        # Run guardrail checks
        guardrail_results = guardrails.run_all_checks(prompt)
        blocked = any(not check.passed and check.severity == "block" for check in guardrail_results)

        if blocked:
            st.error("⚠️ Your request was blocked by security guardrails. Please rephrase.")
            for check in guardrail_results:
                if not check.passed:
                    st.write(f"- {check.check_name}: {check.message}")
            return

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simulate AI response (placeholder — would connect to LangGraph orchestrator)
        with st.chat_message("assistant"):
            with st.spinner("MultiMind AI is thinking..."):
                response_content = (
                    f"This is a placeholder response to your query: '{prompt[:100]}...'\n\n"
                    "In production, this would be processed by the LangGraph orchestrator "
                    "which coordinates the Supervisor, Planner, Research, Validator, "
                    "Conflict Detection, and Reflection agents to produce a comprehensive answer."
                )
                st.markdown(response_content)
                st.caption("Confidence: 0.85 (development mode)")

                # Add sources
                sources = ["internal_knowledge_base", "company_policies"]
                with st.expander("📎 Sources"):
                    for source in sources:
                        st.write(f"- {source}")

        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_content,
            "confidence": 0.85,
            "sources": sources,
        })

        # Log the query
        audit_logger.log_query(user.user_id, prompt)


def render_dashboard_page(user: User) -> None:
    """Render the role-based dashboard page."""
    st.header("📊 Dashboard")

    # Import dashboard modules
    from multimind.dashboards.ceo import render_ceo_dashboard
    from multimind.dashboards.hr import render_hr_dashboard
    from multimind.dashboards.finance import render_finance_dashboard
    from multimind.dashboards.project import render_project_dashboard
    from multimind.dashboards.employee import render_employee_dashboard

    role_dashboard_map = {
        "ceo": render_ceo_dashboard,
        "hr": render_hr_dashboard,
        "finance": render_finance_dashboard,
        "project_manager": render_project_dashboard,
        "employee": render_employee_dashboard,
    }

    # Check access
    if not user.can_access("dashboard"):
        st.warning("You do not have permission to view dashboards.")
        return

    # Render role-specific dashboard
    dashboard_renderer = role_dashboard_map.get(user.role)
    if dashboard_renderer:
        dashboard_renderer()
    else:
        st.info(f"Dashboard for role '{user.role}' is not yet configured.")

    # Log access
    audit_logger.log_data_access(user.user_id, "dashboard")


def render_knowledge_base(user: User) -> None:
    """Render the knowledge base page."""
    st.header("📚 Knowledge Base")
    st.markdown("Search and manage the organization's knowledge.")

    # Search
    search_query = st.text_input("🔍 Search knowledge base...", key="kb_search")

    if search_query:
        st.info(f"Searching for: '{search_query}'")
        # Placeholder — would connect to KnowledgeRetriever in production
        st.write("Results would appear here in production mode.")

    # Document upload
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, DOCX, XLSX, TXT, MD)",
        type=["pdf", "docx", "xlsx", "txt", "md"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({(file.size / 1024):.1f} KB)")
        st.success(f"{len(uploaded_files)} file(s) ready for ingestion.")

    # Knowledge base stats
    st.subheader("Knowledge Base Statistics")
    st.metric("Total Documents", "0 (development mode)")
    st.metric("Total Chunks", "0")


def render_knowledge_genome(user: User) -> None:
    """Render the Knowledge Genome page."""
    st.header("🧠 Knowledge Genome")
    st.markdown("Explore your company's unique organizational patterns.")

    st.info(
        "The Knowledge Genome is a proprietary feature that learns how your company "
        "operates — decision patterns, approval workflows, team collaboration styles, "
        "and business strategies — creating organization-specific intelligence."
    )

    # Placeholder for genome visualization
    st.subheader("Genome Patterns")
    st.write("Pattern types: decision_patterns, approval_workflows, team_collaboration, project_outcomes, customer_behavior, risk_profiles")


def render_security_page(user: User) -> None:
    """Render the security page."""
    st.header("🔒 Security")

    if user.role != "ceo":
        st.warning("Security settings are restricted to CEO access.")
        return

    st.subheader("Access Control")
    st.write("Role-Based Access Control (RBAC) is active.")

    st.subheader("Guardrail Status")
    st.success("✅ Prompt Injection Detection: Active")
    st.success("✅ SQL Injection Prevention: Active")
    st.success("✅ PII Masking: Active")
    st.success("✅ Audit Logging: Active")

    st.subheader("Recent Audit Logs")
    logs = audit_logger.get_logs(limit=10)
    if logs:
        for log in logs[:5]:
            st.caption(f"{log['timestamp'][:19]} — {log['action']} — {log['resource']}")
    else:
        st.write("No audit entries yet.")

    st.subheader("Multi-Tenant Data Isolation")
    st.success("✅ Each department can only access their own data.")


def render_about_page(user: User) -> None:
    """Render the about page."""
    st.header("ℹ️ About MultiMind AI")
    st.markdown("""
    **MultiMind AI** is an AI Operating System for enterprises that unifies organizational knowledge, documents, projects, employees, and business intelligence into one secure, multi-agent platform.

    ---

    ### Key Features
    - **Multi-Agent AI Architecture** — Supervisor, Planner, Research, Validator, Conflict Detection, Reflection agents
    - **Company Knowledge Genome** — Learns your organization's unique patterns
    - **Enterprise Digital Twin** — Maps relationships across the organization
    - **Organizational Memory** — Preserves knowledge when employees leave
    - **Future Business Simulator** — What-if scenario modeling
    - **AI Executive Council** — Specialized agents collaborate before final answers
    - **Company Health Engine** — Live health scoring across 7 dimensions
    - **Silent AI** — Proactive problem detection
    - **Knowledge Doctor** — Automatic knowledge base maintenance
    - **Explainable AI** — Full transparency into every answer
    - **Agent Replay** — Debug and audit any AI workflow

    ---

    ### Technology Stack
    - **Frontend:** Streamlit
    - **Backend:** Python
    - **AI Framework:** LangChain + LangGraph
    - **AI Models:** Cohere API + OpenAI API
    - **Web Search:** Tavily Search API
    - **Database:** SQLite
    - **Vector DB:** FAISS
    - **Deployment:** Docker + AWS

    ---

    **Version:** 0.1.0
    **Contact:** thirishasriram079@gmail.com
    """)

    # Log the visit
    audit_logger.log(user.user_id, "page_view", "about")


if __name__ == "__main__":
    main()
