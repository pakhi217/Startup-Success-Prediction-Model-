import streamlit as st
import streamlit.components.v1 as components
import textwrap

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# THEME
# --------------------------------------------------
st.markdown("""
<style>

    .stApp {
        background:
            radial-gradient(circle at 12% 15%, rgba(124,58,237,0.14), transparent 38%),
            radial-gradient(circle at 88% 8%, rgba(37,99,235,0.14), transparent 38%),
            radial-gradient(circle at 50% 95%, rgba(34,211,238,0.08), transparent 40%),
            #0a0e1a;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #0d1220;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] div.stButton > button {
        background: #10192b !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        padding: 0.6em 1em !important;
        justify-content: flex-start !important;
        text-align: left !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        background: #16213a !important;
        border-color: rgba(255,255,255,0.12) !important;
        color: #f8fafc !important;
    }

    .nav-active {
        background: linear-gradient(90deg, rgba(56,189,248,0.16), rgba(168,85,247,0.10)) !important;
        border: 1px solid rgba(56,189,248,0.4) !important;
        border-left: 3px solid #38BDF8 !important;
        border-radius: 10px;
        padding: 0.6rem 1rem 0.6rem 0.85rem;
        margin-bottom: 6px;
        font-weight: 700;
        color: #38BDF8 !important;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .version-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        color: #2DD4BF;
        background: rgba(45,212,191,0.10);
        border: 1px solid rgba(45,212,191,0.28);
        padding: 3px 10px;
        border-radius: 999px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in { animation: fadeUp 0.7s ease both; }
    .fade-in-1 { animation: fadeUp 0.7s ease 0.05s both; }
    .fade-in-2 { animation: fadeUp 0.7s ease 0.15s both; }
    .fade-in-3 { animation: fadeUp 0.7s ease 0.25s both; }

    .badge-pill {
        display: inline-block;
        background: rgba(168,85,247,0.12);
        border: 1px solid rgba(168,85,247,0.35);
        color: #c4b5fd;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 5px 16px;
        border-radius: 999px;
        margin-bottom: 16px;
    }

    .gradient-title-left {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(90deg, #60a5fa, #a855f7, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -0.01em;
    }

    .tagline-left {
        color: #cbd5e1;
        font-size: 16.5px;
        line-height: 1.7;
        margin-bottom: 10px;
        max-width: 560px;
    }

    .tagline-sub {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.7;
        max-width: 560px;
    }

    .accent-bar-left {
        width: 70px;
        height: 4px;
        border-radius: 4px;
        background: linear-gradient(90deg, #7c3aed, #22d3ee);
        margin-bottom: 18px;
    }

    .section-heading {
        color: #f8fafc;
        font-weight: 700;
        font-size: 22px;
        border-left: 4px solid #7c3aed;
        padding-left: 12px;
        margin: 36px 0 18px 0;
    }

    .card {
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }

    .card:hover {
        transform: translateY(-8px);
        border-color: rgba(168,85,247,0.45);
        box-shadow: 0 14px 30px rgba(124,58,237,0.28);
    }

    .problem-card { border-left: 3px solid #f97316; }
    .solution-card { border-left: 3px solid #22d3ee; }

    .icon-badge {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-bottom: 12px;
    }

    .badge-purple { background: rgba(168,85,247,0.16); }
    .badge-blue   { background: rgba(59,130,246,0.16); }
    .badge-teal   { background: rgba(45,212,191,0.16); }
    .badge-coral  { background: rgba(251,146,60,0.16); }
    .badge-orange { background: rgba(249,115,22,0.16); }
    .badge-cyan   { background: rgba(34,211,238,0.16); }

    .card-title { font-weight: 700; color: #f8fafc; font-size: 16.5px; margin-bottom: 8px; }
    .card-text { color: #94a3b8; font-size: 13.5px; line-height: 1.7; }

    .team-chip {
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .team-chip:hover {
        transform: translateY(-6px);
        border-color: rgba(168,85,247,0.45);
    }

    .team-avatar {
        width: 38px; height: 38px; border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; color: white; font-size: 14px; flex-shrink: 0;
    }

    footer, #MainMenu {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


def info_card(icon, title, text, color="purple", cls="fade-in"):
    st.markdown(textwrap.dedent(f"""
    <div class="card {cls}">
        <div class="icon-badge badge-{color}">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-text">{text}</div>
    </div>
    """), unsafe_allow_html=True)


def styled_card(icon, title, text, color="purple", side_class="", cls="fade-in"):
    st.markdown(textwrap.dedent(f"""
    <div class="card {side_class} {cls}">
        <div class="icon-badge badge-{color}">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-text">{text}</div>
    </div>
    """), unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding:0.6rem 0 1rem 0;">
            <div style="font-family:'Manrope','Inter',sans-serif; font-weight:700; font-size:1.5rem; color:#F8FAFC; letter-spacing:-0.01em;">Startup Success Predictor</div>
            <div style="font-size:0.72rem; color:#94A3B8; letter-spacing:0.02em;">Startup Analytics Platform</div>
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:1.4rem;">
            <span class="version-badge">✓ Machine Learning Model </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.1em; "
        "text-transform:uppercase; color:#94A3B8; margin-bottom:0.6rem;'>Navigation</div>",
        unsafe_allow_html=True,
    )

    nav_items = [("🏠", "Home"), ("📊", "Dashboard"), ("📈", "Analytics"), ("🔍", "Explorer"), ("🤖", "Prediction"), ("ℹ️", "About")]
    page_map = {
        "Home": "Home.py",
        "Dashboard": "Dashboard.py",
        "Analytics": "Analytics.py",
        "Explorer": "Explorer.py",
        "Prediction": "Prediction.py",
        "About": "About.py",
    }
    for icon, label in nav_items:
        if label == "About":
            st.markdown(f'<div class="nav-active">{icon} &nbsp;{label}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{icon}   {label}", key=f"nav_{label}", use_container_width=True):
                st.switch_page(f"pages/{page_map[label]}")
    st.markdown("---")
    st.caption("Version 1.0")

# --------------------------------------------------
# HEADER + VALUE PROPOSITION
# --------------------------------------------------
hero_l, hero_r = st.columns([1.15, 1], gap="large")

with hero_l:
    st.markdown('<div class="badge-pill fade-in">ABOUT THE PLATFORM</div>', unsafe_allow_html=True)
    st.markdown('<div class="gradient-title-left fade-in">About This Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-bar-left fade-in-1"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline-left fade-in-1">Every year, thousands of promising startups fail — '
        'not always from bad ideas, but from decisions made without enough visibility into what '
        'actually predicts success.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="tagline-sub fade-in-2">Our mission is to democratize access to venture data '
        'insight — giving founders, investors, and incubators the same pattern-based visibility '
        'once reserved for large VC firms, through a transparent, data-driven prediction model.</div>',
        unsafe_allow_html=True
    )

with hero_r:
    components.html("""
    <style> html, body { margin:0; padding:0; background:transparent; } </style>
    <div style="display:flex; align-items:center; justify-content:center;">
    <svg viewBox="0 0 500 380" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-height:360px;">
        <defs>
            <radialGradient id="orbGlow" cx="50%" cy="45%" r="55%">
                <stop offset="0%" stop-color="#a855f7" stop-opacity="0.55"/>
                <stop offset="55%" stop-color="#2563eb" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="#0a0e1a" stop-opacity="0"/>
            </radialGradient>
            <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#22d3ee"/>
                <stop offset="50%" stop-color="#60a5fa"/>
                <stop offset="100%" stop-color="#a855f7"/>
            </linearGradient>
            <radialGradient id="coreGrad" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff"/>
                <stop offset="40%" stop-color="#60a5fa"/>
                <stop offset="100%" stop-color="#7c3aed"/>
            </radialGradient>
        </defs>
        <circle cx="250" cy="180" r="200" fill="url(#orbGlow)"/>
        <ellipse cx="250" cy="180" rx="150" ry="55" fill="none" stroke="url(#ringGrad)" stroke-width="1.4" opacity="0.55">
            <animateTransform attributeName="transform" type="rotate" from="-18 250 180" to="342 250 180" dur="14s" repeatCount="indefinite"/>
        </ellipse>
        <ellipse cx="250" cy="180" rx="120" ry="120" fill="none" stroke="url(#ringGrad)" stroke-width="1" opacity="0.35">
            <animateTransform attributeName="transform" type="rotate" from="0 250 180" to="-360 250 180" dur="20s" repeatCount="indefinite"/>
        </ellipse>
        <circle cx="250" cy="180" r="42" fill="url(#coreGrad)" opacity="0.95">
            <animate attributeName="r" values="42;46;42" dur="3s" repeatCount="indefinite"/>
        </circle>
        <circle cx="130" cy="110" r="7" fill="#22d3ee"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.5s" repeatCount="indefinite"/></circle>
        <circle cx="370" cy="100" r="6" fill="#a855f7"><animate attributeName="opacity" values="1;0.4;1" dur="2.2s" repeatCount="indefinite"/></circle>
        <circle cx="100" cy="250" r="6" fill="#60a5fa"><animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/></circle>
        <circle cx="390" cy="260" r="7" fill="#22d3ee"><animate attributeName="opacity" values="1;0.5;1" dur="2.7s" repeatCount="indefinite"/></circle>
    </svg>
    </div>
    """, height=360)

st.write("")

# --------------------------------------------------
# THE PROBLEM AND SOLUTION
# --------------------------------------------------
st.markdown('<div class="section-heading">⚡ The Problem &amp; Our Solution</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2)
with p1:
    styled_card("⚠️", "The Problem",
        "Up to 90% of startups fail — wasting massive amounts of capital, time, and talent. "
        "Much of that failure traces back to decisions made without enough visibility into the "
        "patterns that actually separate successful ventures from the rest.",
        color="orange", side_class="problem-card", cls="fade-in-1")
with p2:
    styled_card("💡", "Our Solution",
        "A machine learning model trained on historical startup data that evaluates funding, "
        "industry, and market signal patterns to estimate a startup's likelihood of long-term "
        "viability — turning guesswork into a data-backed signal.",
        color="cyan", side_class="solution-card", cls="fade-in-2")

st.write("")
st.markdown('<div class="section-heading" style="margin-top:10px;">🎯 Who It\'s For</div>', unsafe_allow_html=True)

u1, u2, u3 = st.columns(3)
with u1:
    info_card("🚀", "Founders",
        "Benchmark your startup against historical patterns and understand what data-driven "
        "investors are actually looking for.",
        color="purple", cls="fade-in-1")
with u2:
    info_card("💰", "Investors",
        "Screen opportunities faster with a consistent, data-backed second opinion alongside "
        "your own due diligence.",
        color="blue", cls="fade-in-2")
with u3:
    info_card("🏢", "Incubators",
        "Track and compare portfolio companies at scale, spotting risk patterns early across "
        "your cohort.",
        color="teal", cls="fade-in-3")

# --------------------------------------------------
# HOW IT WORKS — ML PIPELINE ILLUSTRATION
# --------------------------------------------------
st.markdown('<div class="section-heading">🧭 How It Works — The ML Pipeline</div>', unsafe_allow_html=True)

components.html("""
<style>
    html, body { margin:0; padding:0; background:transparent; }

    .pipeline-wrap {
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 30px 10px 10px 10px;
    }

    .pipeline-line {
        position: absolute;
        top: 50px;
        left: 40px;
        right: 40px;
        height: 2px;
        background: linear-gradient(90deg, #7c3aed, #2563eb, #22d3ee);
        opacity: 0.3;
    }

    .particle {
        position: absolute;
        top: 44px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 10px 3px rgba(34,211,238,0.7);
        animation: travel 5s linear infinite;
    }

    @keyframes travel {
        0%   { left: 40px; opacity: 0; }
        8%   { opacity: 1; }
        92%  { opacity: 1; }
        100% { left: calc(100% - 50px); opacity: 0; }
    }

    .node {
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100px;
    }

    .node-circle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: #10192b;
        border: 2px solid #7c3aed;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 16px rgba(124,58,237,0.35);
        animation: pulseNode 3s ease-in-out infinite;
    }

    .node-circle.final {
        border-color: #22d3ee;
        box-shadow: 0 0 20px rgba(34,211,238,0.5);
    }

    @keyframes pulseNode {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }

    .node-label {
        margin-top: 10px;
        font-size: 12.5px;
        font-weight: 600;
        color: #cbd5e1;
        text-align: center;
        line-height: 1.3;
    }
</style>

<div class="pipeline-wrap">
    <div class="pipeline-line"></div>
    <div class="particle" style="animation-delay: 0s;"></div>
    <div class="particle" style="animation-delay: 1.7s;"></div>
    <div class="particle" style="animation-delay: 3.4s;"></div>

    <div class="node">
        <div class="node-circle" style="animation-delay:0s;">🗂️</div>
        <div class="node-label">Data Sources</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:0.3s;">🧹</div>
        <div class="node-label">Cleaning</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:0.6s;">📊</div>
        <div class="node-label">EDA</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:0.9s;">🧩</div>
        <div class="node-label">Feature Engineering</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:1.2s;">⚙️</div>
        <div class="node-label">Preprocess</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:1.5s;">🤖</div>
        <div class="node-label">Model Training</div>
    </div>
    <div class="node">
        <div class="node-circle" style="animation-delay:1.8s;">📈</div>
        <div class="node-label">Evaluation</div>
    </div>
    <div class="node">
        <div class="node-circle final" style="animation-delay:2.1s;">🔮</div>
        <div class="node-label">Prediction</div>
    </div>

</div>
""", height=190)
st.write("")

h1, h2, h3 = st.columns(3)
with h1:
    info_card("🗂️", "Data Sources",
        "Trained on the Crunchbase Startup Success/Failure Dataset (via Kaggle) — aggregated "
        "profiles covering funding, industry, and outcome data across historical startups.",
        color="purple", cls="fade-in-1")
with h2:
    info_card("🔍", "Key Features Analyzed",
        "Variables like funding amount, funding rounds, industry category, country/region, "
        "and company founding and funding dates feed into the model.",
        color="coral", cls="fade-in-2")
with h3:
    info_card("🧠", "Model Transparency",
        "Multiple classification algorithms — Logistic Regression, Decision Tree, Random Forest, "
        "and Gradient Boosting — were trained and compared, with the strongest performer selected "
        "as the final model. Data was cleaned and balanced beforehand to reduce bias from missing "
        "or skewed entries.",
        color="blue", cls="fade-in-3")

# --------------------------------------------------
# TEAM
# --------------------------------------------------
st.markdown('<div class="section-heading">👥 Team Members</div>', unsafe_allow_html=True)

team = ["Aanya Gupta", "Himanshi Gupta", "Pakhi Saxena", "Jiya Adhikari", "Jigyasa Chuphal"]
cols = st.columns(len(team))
for i, (col, name) in enumerate(zip(cols, team)):
    with col:
        initials = "".join([n[0] for n in name.split()[:2]])
        fade_cls = f"fade-in-{(i % 3) + 1}"
        st.markdown(textwrap.dedent(f"""
        <div class="team-chip {fade_cls}">
            <div class="team-avatar">{initials}</div>
            <div class="card-title" style="margin-bottom:0; font-size:13.5px;">{name}</div>
        </div>
        """), unsafe_allow_html=True)

st.write("")
st.markdown("---")
st.markdown('<div style="text-align:center; color:#64748b; font-size:12px;">© 2026 Startup Success Analytics Platform · All Rights Reserved</div>', unsafe_allow_html=True)