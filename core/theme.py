"""
MultiMind AI visual theme — "Instrument Panel" design system.

Design concept: MultiMind AI is a living control room for an organization.
The UI borrows from analog instrument panels and early terminal displays —
amber phosphor readouts, hairline panel dividers, monospace data labels —
rather than a generic SaaS dashboard look. The signature element is the
Agent Pipeline strip: a physical-feeling chain of status lights that lights
up amber as each agent completes its work, echoing a terminal boot sequence.

This module only builds CSS + HTML strings; it has no Streamlit state of
its own so it can be imported anywhere.
"""

# Design tokens
BG = "#0B0E12"
PANEL = "#141920"
PANEL_ALT = "#181E26"
BORDER = "#262C34"
TEXT = "#ECEFF3"
MUTED = "#848D97"
ACCENT = "#E8B04B"
ACCENT_DIM = "#8A6A2E"
TEAL = "#3FBF9E"
DANGER = "#E5635A"
FONT_MONO = "'JetBrains Mono', 'Courier New', monospace"
FONT_BODY = "'Inter', -apple-system, sans-serif"

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: {FONT_BODY};
}}

.stApp {{
    background: {BG};
    color: {TEXT};
}}

section[data-testid="stSidebar"] {{
    background: {PANEL};
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT};
}}

h1, h2, h3 {{
    font-family: {FONT_MONO};
    letter-spacing: 0.02em;
    color: {TEXT};
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {FONT_MONO};
    font-size: 0.85rem;
    color: {MUTED};
    background: transparent;
}}
.stTabs [aria-selected="true"] {{
    color: {ACCENT} !important;
    border-bottom: 2px solid {ACCENT} !important;
}}

.stButton > button {{
    font-family: {FONT_MONO};
    background: {PANEL_ALT};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 3px;
}}
.stButton > button:hover {{
    border-color: {ACCENT};
    color: {ACCENT};
}}
.stButton > button[kind="primary"] {{
    background: {ACCENT};
    color: #171208;
    border: 1px solid {ACCENT};
    font-weight: 600;
}}
.stButton > button[kind="primary"]:hover {{
    background: #f0bd63;
    color: #171208;
}}

.stTextInput input, .stTextInput textarea {{
    background: {PANEL_ALT} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    font-family: {FONT_MONO};
}}

div[data-testid="stAlertContainer"] {{
    border-radius: 3px;
    border: 1px solid {BORDER};
    font-family: {FONT_BODY};
}}

/* ---- Custom console components ---- */

.mm-topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 4px;
    margin-bottom: 18px;
    font-family: {FONT_MONO};
    font-size: 0.8rem;
    color: {MUTED};
}}
.mm-topbar .dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: {TEAL};
    margin-right: 6px;
    box-shadow: 0 0 6px {TEAL};
}}
.mm-topbar strong {{ color: {TEXT}; }}

.mm-card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 10px;
    margin-bottom: 14px;
}}
.mm-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-left: 3px solid {ACCENT};
    border-radius: 3px;
    padding: 12px 14px;
}}
.mm-card .label {{
    font-family: {FONT_MONO};
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {MUTED};
    margin-bottom: 6px;
}}
.mm-card .value {{
    font-family: {FONT_MONO};
    font-size: 1.5rem;
    font-weight: 700;
    color: {TEXT};
}}
.mm-card.tone-good {{ border-left-color: {TEAL}; }}
.mm-card.tone-warn {{ border-left-color: {ACCENT}; }}
.mm-card.tone-bad {{ border-left-color: {DANGER}; }}

.mm-panel {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 14px 16px;
    margin-bottom: 14px;
}}
.mm-panel .note {{
    font-size: 0.9rem;
    color: {MUTED};
    border-left: 2px solid {BORDER};
    padding-left: 10px;
    margin-top: 8px;
}}

.mm-healthbar-track {{
    background: {PANEL_ALT};
    border: 1px solid {BORDER};
    border-radius: 3px;
    height: 10px;
    width: 100%;
    overflow: hidden;
}}
.mm-healthbar-fill {{
    height: 100%;
    background: linear-gradient(90deg, {ACCENT_DIM}, {ACCENT});
}}

.mm-pipeline {{
    display: flex;
    align-items: center;
    padding: 18px 10px;
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 4px;
    margin-bottom: 14px;
    overflow-x: auto;
}}
.mm-pipe-node {{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 92px;
    font-family: {FONT_MONO};
    font-size: 0.68rem;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    text-align: center;
}}
.mm-pipe-light {{
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: {PANEL_ALT};
    border: 2px solid {BORDER};
    margin-bottom: 6px;
}}
.mm-pipe-node.done .mm-pipe-light {{
    background: {ACCENT};
    border-color: {ACCENT};
    box-shadow: 0 0 8px {ACCENT};
}}
.mm-pipe-node.done {{ color: {TEXT}; }}
.mm-pipe-node.flagged .mm-pipe-light {{
    background: {DANGER};
    border-color: {DANGER};
    box-shadow: 0 0 8px {DANGER};
}}
.mm-pipe-node.flagged {{ color: {DANGER}; }}
.mm-pipe-connector {{
    flex: 1;
    height: 2px;
    background: {BORDER};
    min-width: 20px;
    margin: 0 2px;
    margin-bottom: 20px;
}}
.mm-pipe-connector.done {{ background: {ACCENT}; }}

.mm-trace-step {{
    border: 1px solid {BORDER};
    border-radius: 3px;
    padding: 10px 12px;
    margin-bottom: 8px;
    background: {PANEL_ALT};
}}
.mm-trace-step .agent-name {{
    font-family: {FONT_MONO};
    color: {ACCENT};
    font-size: 0.82rem;
    font-weight: 700;
    margin-bottom: 4px;
}}
.mm-trace-step .io-line {{
    font-size: 0.82rem;
    color: {MUTED};
    margin: 2px 0;
}}

.mm-badge {{
    display: inline-block;
    font-family: {FONT_MONO};
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid {BORDER};
    color: {MUTED};
}}
.mm-badge.role {{
    color: {ACCENT};
    border-color: {ACCENT_DIM};
}}
</style>
"""


def inject_theme(st):
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def topbar_html(role: str, username: str, doc_count: int, chunk_count: int) -> str:
    return f"""
    <div class="mm-topbar">
        <div><span class="dot"></span><strong>MULTIMIND AI</strong> — session active</div>
        <div>role: <strong>{role}</strong> ({username}) &nbsp;|&nbsp; docs indexed: <strong>{doc_count}</strong> &nbsp;|&nbsp; chunks: <strong>{chunk_count}</strong></div>
    </div>
    """


def kpi_cards_html(kpis: list, tones: list = None) -> str:
    tones = tones or ["neutral"] * len(kpis)
    cards = "".join(
        f'<div class="mm-card tone-{tone}"><div class="label">{label}</div>'
        f'<div class="value">{value}</div></div>'
        for (label, value), tone in zip(kpis, tones)
    )
    return f'<div class="mm-card-grid">{cards}</div>'


def health_bar_html(score: int) -> str:
    return f"""
    <div class="mm-healthbar-track">
        <div class="mm-healthbar-fill" style="width:{score}%"></div>
    </div>
    """


PIPELINE_AGENTS = ["Supervisor", "Planner", "Research", "Conflict", "Draft", "Validator"]


def pipeline_html(trace: list, conflict_flagged: bool = False) -> str:
    completed_names = {step["agent"].replace(" Agent", "") for step in trace}
    nodes = []
    for i, name in enumerate(PIPELINE_AGENTS):
        is_done = name in completed_names or any(name in c for c in completed_names)
        is_flagged = conflict_flagged and name == "Conflict"
        cls = "done" if is_done else ""
        if is_flagged:
            cls = "flagged"
        nodes.append(f'<div class="mm-pipe-node {cls}"><div class="mm-pipe-light"></div>{name}</div>')
        if i < len(PIPELINE_AGENTS) - 1:
            connector_done = is_done
            nodes.append(f'<div class="mm-pipe-connector {"done" if connector_done else ""}"></div>')
    return f'<div class="mm-pipeline">{"".join(nodes)}</div>'


def trace_step_html(agent: str, input_summary: str, output_summary: str) -> str:
    return f"""
    <div class="mm-trace-step">
        <div class="agent-name">{agent}</div>
        <div class="io-line">input: {input_summary}</div>
        <div class="io-line">output: {output_summary}</div>
    </div>
    """
