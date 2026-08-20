import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

.stApp {
    background: #0d1117;
    background-image:
        radial-gradient(ellipse 70% 45% at 10% 0%, rgba(99,102,241,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(6,182,212,0.07) 0%, transparent 50%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 5rem; max-width: 1200px; }

/* Hero */
.hero {
    text-align: center;
    padding: 4rem 0 2.5rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.2rem);
    font-weight: 700;
    line-height: 1.05;
    letter-spacing: -0.035em;
    color: #f1f5f9;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #818cf8 0%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 400;
    color: #64748b;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.25), rgba(6,182,212,0.15), transparent);
    margin: 2rem 0;
}

/* Input card */
.input-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}

/* Input overrides */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 9px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.13) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #475569 !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #818cf8 !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.30) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(99,102,241,0.40) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(99,102,241,0.30) !important;
    color: #818cf8 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.4rem !important;
    transition: background 0.2s, border-color 0.2s !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,102,241,0.08) !important;
    border-color: rgba(99,102,241,0.50) !important;
    transform: none !important;
}

/* Step cards */
.step-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(99,102,241,0.40);
    background: rgba(99,102,241,0.05);
}
.step-card.done {
    border-color: rgba(34,197,94,0.28);
    background: rgba(34,197,94,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #818cf8; }
.step-card.done::before   { background: #22c55e; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #475569;
}
.step-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #e2e8f0;
}
.step-desc {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 0.2rem;
    margin-left: calc(0.75rem + 2.4rem);
}
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.1em;
}
.status-waiting { color: #334155; }
.status-running { color: #818cf8; }
.status-done    { color: #22c55e; }

/* Result panels */
.result-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-top: 0.75rem;
    margin-bottom: 1.2rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 1rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid rgba(99,102,241,0.12);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.85;
    color: #94a3b8;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* Report & feedback panels */
.report-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(99,102,241,0.20);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.65rem;
}
.panel-label.indigo {
    color: #818cf8;
    border-bottom: 1px solid rgba(99,102,241,0.14);
}
.panel-label.green {
    color: #22c55e;
    border-bottom: 1px solid rgba(34,197,94,0.14);
}

/* Section heading */
.section-heading {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 1.2rem;
}

/* Example chips */
.chip {
    display: inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 6px;
    padding: 0.22rem 0.65rem;
    font-size: 0.73rem;
    color: #64748b;
    font-family: 'Inter', sans-serif;
    margin-right: 0.4rem;
}

/* Spinner */
.stSpinner > div { color: #818cf8 !important; }

/* Expander */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #475569 !important;
    letter-spacing: 0.08em !important;
    cursor: pointer;
}

/* Warning */
.stAlert { border-radius: 10px !important; }

/* Footer */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: #1e293b;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)


def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    desc_html = f'<div class="step-desc">{desc}</div>' if desc else ""
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#334155;letter-spacing:0.12em;">TRY →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None

    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label indigo">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)