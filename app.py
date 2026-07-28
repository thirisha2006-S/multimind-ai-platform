"""MultiMind AI — Polished Instrument Panel Startup Frontend."""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from multimind.utils.config import settings
from multimind.utils.logger import get_logger
from multimind.security.auth import Authenticator
from multimind.security.guardrails import Guardrails
from multimind.security.audit import AuditLogger
from multimind.agents.orchestrator import run_pipeline

logger = get_logger(__name__)
st.set_page_config(page_title="MultiMind AI", page_icon="🧠", layout="wide")

# ── Instrument Panel Theme ──
st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp { background: #0F172A; color: #F8FAFC; font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { background: #0B0E12 !important; border-right: 1px solid #262C34; }
[data-testid="stSidebar"] * { color: #F8FAFC; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; padding: 0 16px; border-bottom: 1px solid #262C34; }
.stTabs [data-baseweb="tab"] { font-family: monospace; font-size: 0.78rem; color: #94A3B8; background: transparent; padding: 8px 14px; border-radius: 6px 6px 0 0; }
.stTabs [aria-selected="true"] { color: #F8FAFC !important; border-bottom: 2px solid #3B82F6 !important; background: #1A2030 !important; }
.stButton > button { font-family: monospace; background: #1A2030; color: #F8FAFC; border: 1px solid #262C34; border-radius: 6px; padding: 6px 16px; font-size: 0.82rem; }
.stButton > button:hover { border-color: #3B82F6; color: #3B82F6; }
.stButton > button[kind="primary"] { background: #3B82F6; color: #fff; border-color: #3B82F6; font-weight: 600; }
.stButton > button[kind="primary"]:hover { background: #2563EB; }
.stTextInput input { background: #1A2030 !important; color: #F8FAFC !important; border: 1px solid #262C34 !important; border-radius: 6px; font-family: monospace; padding: 8px 12px !important; }
.stTextInput textarea { background: #1A2030 !important; color: #F8FAFC !important; border: 1px solid #262C34 !important; border-radius: 6px; font-family: monospace; padding: 8px 12px !important; }
div[data-testid="stAlertContainer"] { border-radius: 6px; border: 1px solid #262C34; background: #1A2030; }
.stMetric { background: #141920; border: 1px solid #262C34; border-radius: 8px; padding: 12px; text-align: center; }
.stMetric h3 { font-size: 1.1rem; margin: 0; }
.stMetric label { font-size: 0.7rem; color: #94A3B8; }
</style>""",
    unsafe_allow_html=True,
)

authenticator = Authenticator()
audit_logger = AuditLogger()
guardrails = Guardrails()


def check_auth():
    if "user" not in st.session_state:
        st.session_state.user = None
    user = st.session_state.user

    if user is None:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2.5, 1])
        with c2:
            st.markdown(
                '<div style="text-align:center; padding:20px 0;">'
                '<div style="font-size:2.2rem; font-weight:800;">MultiMind AI</div>'
                '<div style="font-size:.85rem; color:#94A3B8; font-family:monospace;">The AI Operating System for Enterprise</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            with st.form("login"):
                email = st.text_input("Email", placeholder="you@company.com", key="email", label_visibility="collapsed")
                password = st.text_input("Password", type="password", placeholder="Enter password", key="pass", label_visibility="collapsed")
                submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            if submitted:
                username = email.split("@")[0] if "@" in email else email
                user_obj = authenticator.register_user(
                    username=username, password=password, role="employee",
                    email=email, department="Engineering",
                )
                user = {
                    "user_id": user_obj.user_id,
                    "username": user_obj.username,
                    "role": user_obj.role,
                    "email": user_obj.email,
                    "department": user_obj.department,
                }
                st.session_state.user = user
                audit_logger.log_login(user["user_id"], success=True)
                st.rerun()
            st.caption("Secure Enterprise Login")
            with st.expander("Demo credentials"):
                st.code("Email: ceo@multimind.ai  |  Password: ceo123  |  Role: CEO")
        st.stop()
    return st.session_state.user


def render_sidebar(user):
    with st.sidebar:
        st.markdown("### MultiMind AI")
        st.markdown(f"**{user.get('username', 'User')}**")
        st.caption(user.get("role", "").upper())
        st.markdown("---")
        page = st.radio(
            "",
            [
                "Dashboard",
                "AI Chat",
                "Documents",
                "Employees",
                "Projects",
                "Finance",
                "HR",
                "Clients",
                "Tasks",
                "Analytics",
                "Knowledge Genome",
                "Knowledge Doctor",
                "Notifications",
                "Settings",
            ],
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.text_input("API Key", type="password", key="api")
        st.markdown("---")
        if st.button("Log Out", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    return page


def render_dashboard(user):
    st.markdown("# Good Morning, Thirisha 👋")
    st.markdown("### Company Health")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Employees", "528")
    with c2:
        st.metric("Projects", "38")
    with c3:
        st.metric("Clients", "82")
    with c4:
        st.metric("Revenue", "$1.8M")
    st.markdown("---")
    st.subheader("AI Insights")
    st.write("- Project Alpha at risk")
    st.write("- HR hiring below target")
    st.write("- Revenue increasing 8%")


def render_chat(user):
    st.markdown("# AI Chat")
    st.markdown("#### MultiMind AI")
    st.caption("How can I help your organization today?")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.write(f"- {s}")
            if msg.get("confidence"):
                st.caption(f"Confidence: {msg['confidence']}%")

    if prompt := st.chat_input("Message MultiMind AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = run_pipeline(query=prompt, context={})
                    answer = result.get("answer", "No answer.")
                    conf = result.get("confidence", 85)
                    sources = result.get("sources", [])
                    st.markdown(answer)
                    if sources:
                        with st.expander("Sources"):
                            for s in sources:
                                st.write(f"- {s}")
                    st.caption(f"Confidence: {conf}%")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "confidence": conf}
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
        audit_logger.log_query(user.get("user_id", "anon"), prompt)


def render_docs(user):
    st.markdown("# Documents")
    uploaded = st.file_uploader(
        "Upload documents",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )
    if uploaded:
        for f in uploaded:
            st.write(f"- {f.name}")
        st.success(f"{len(uploaded)} file(s) ready.")

    for doc in ["HR Policy.pdf", "Leave Policy.pdf", "Sprint Report Q2.pdf"]:
        st.markdown(f"### {doc}")
        st.progress(0.5)


def render_employees(user):
    st.markdown("# Employees")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("### Thirisha Sriram")
        st.caption("AI Engineer | Technology Dept")
        st.write("Manager: John Smith")
    with cols[1]:
        st.metric("Active Projects", "3")
        st.metric("Performance", "92%")
    with cols[2]:
        st.markdown("**Today**")
        st.write("- API Development")
        st.write("- Bug Fix")
        st.write("- Documentation")


def render_projects(user):
    st.markdown("# Projects")
    st.markdown("### Project Alpha")
    st.progress(0.82)
    st.caption("82%")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Deadline", "12 Days Left")
        st.metric("Client", "ABC Corp")
    with c2:
        st.metric("Risk", "Medium")
        st.metric("Budget", "$180K")
    st.info("AI Prediction: Need 2 additional developers")


def render_finance(user):
    st.markdown("# Finance")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Revenue", "$1.8M")
    with c2:
        st.metric("Expenses", "$1.3M")
    with c3:
        st.metric("Cash Flow", "$420K")
    with c4:
        st.metric("ROI", "32%")


def render_hr(user):
    st.markdown("# HR")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total", "528")
    with c2:
        st.metric("New This Month", "12")
    with c3:
        st.metric("Open Positions", "8")


def render_genome(user):
    st.markdown("# Knowledge Genome")
    for name, pct in [("HR", 60), ("Finance", 80), ("Engineering", 100), ("Sales", 50)]:
        st.markdown(f"**{name}**")
        st.progress(pct / 100)
    st.caption("AI Learning Progress: 87%")


def render_kb_doctor(user):
    st.markdown("# Knowledge Doctor")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Health", "91%")
    with c2:
        st.metric("Conflicts", "3")
    with c3:
        st.metric("Outdated", "12")
    with c4:
        st.metric("Duplicates", "6")
    st.markdown("### Recommended Actions")
    for a in ["Update HR Policy", "Archive Leave Policy 2024", "Merge SOP Documents"]:
        st.write(f"- {a}")


def render_notifications(user):
    st.markdown("# Notifications")
    for n in [
        "Project Alpha may miss deadline",
        "Revenue increased 8%",
        "3 New Employees Joined",
        "HR Policy Updated",
    ]:
        st.write(f"- {n}")


def render_settings(user):
    st.markdown("# Settings")
    st.write("Theme: Dark Mode")
    st.write("Language: English")


# ── Main ──
user = check_auth()
page = render_sidebar(user)
st.markdown("---")

route = {
    "Dashboard": render_dashboard,
    "AI Chat": render_chat,
    "Documents": render_docs,
    "Employees": render_employees,
    "Projects": render_projects,
    "Finance": render_finance,
    "HR": render_hr,
    "Clients": lambda u: st.write("Clients page"),
    "Tasks": lambda u: st.write("Tasks page"),
    "Analytics": lambda u: st.line_chart(
        __import__("pandas").DataFrame({"Revenue": [1.2, 1.4, 1.5, 1.6, 1.8]})
    ),
    "Knowledge Genome": render_genome,
    "Knowledge Doctor": render_kb_doctor,
    "Notifications": render_notifications,
    "Settings": render_settings,
}

if page in route:
    route[page](user)
