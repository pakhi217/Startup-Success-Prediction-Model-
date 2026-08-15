import streamlit as st
import streamlit.components.v1 as components
import textwrap

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Startup Success Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# GLOBAL THEME
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

    /* ---------- sidebar (matches Dashboard.py nav) ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15,23,42,0.98) 0%, rgba(11,17,32,0.99) 100%);
        backdrop-filter: blur(18px);
        border-right: 1px solid rgba(148,163,184,0.10);
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        background: rgba(255,255,255,0.02);
        color: #F8FAFC;
        border: 1px solid rgba(148,163,184,0.08);
        border-radius: 12px;
        padding: 0.6rem 1rem;
        margin-bottom: 6px;
        font-weight: 500;
        letter-spacing: 0.01em;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    section[data-testid="stSidebar"] .stButton button::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(56,189,248,0.18), rgba(168,85,247,0.18));
        opacity: 0;
        transition: opacity 0.28s ease;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        border: 1px solid rgba(56,189,248,0.45);
        color: #38BDF8;
        transform: translateX(5px);
        box-shadow: 0 4px 18px rgba(56,189,248,0.18);
    }

    section[data-testid="stSidebar"] .stButton button:hover::before { opacity: 1; }
    section[data-testid="stSidebar"] .stButton button:active { transform: translateX(5px) scale(0.98); }

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

    .nav-item {
        border-radius: 10px;
        padding: 0.6rem 1rem;
        margin-bottom: 6px;
        font-weight: 500;
        color: #94A3B8;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.25s ease;
    }

    .nav-item:hover {
        background: rgba(148,163,184,0.06);
        color: #F8FAFC;
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

    /* ---------- hero ---------- */
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
        margin-bottom: 18px;
    }

    .gradient-title-left {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(90deg, #60a5fa, #a855f7, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 14px;
        letter-spacing: -0.01em;
    }

    .tagline-left {
        color: #cbd5e1;
        font-size: 16.5px;
        line-height: 1.7;
        margin-bottom: 10px;
        max-width: 480px;
    }

    .tagline-sub {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 26px;
        max-width: 480px;
    }

    .accent-bar-left {
        width: 70px;
        height: 4px;
        border-radius: 4px;
        background: linear-gradient(90deg, #7c3aed, #22d3ee);
        margin-bottom: 22px;
    }

    /* ---------- cards ---------- */
    .card {
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 22px 20px;
        height: 100%;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }

    .card:hover {
        transform: translateY(-8px);
        border-color: rgba(168,85,247,0.45);
        box-shadow: 0 14px 30px rgba(124,58,237,0.28);
        cursor: pointer;
    }

    .icon-badge {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
        margin-bottom: 14px;
    }

    .badge-purple { background: rgba(168,85,247,0.16); }
    .badge-blue   { background: rgba(59,130,246,0.16); }
    .badge-teal   { background: rgba(45,212,191,0.16); }
    .badge-coral  { background: rgba(251,146,60,0.16); }

    .card-title {
        font-weight: 700;
        color: #f8fafc;
        font-size: 16px;
        margin-bottom: 6px;
    }

    .card-text {
        color: #94a3b8;
        font-size: 13.5px;
        line-height: 1.55;
    }

    .stagger-down { margin-top: 26px; }

    .section-heading {
        color: #f8fafc;
        font-weight: 700;
        font-size: 22px;
        border-left: 4px solid #7c3aed;
        padding-left: 12px;
        margin: 10px 0 22px 0;
    }

    /* ---------- overview ---------- */
    .overview-box {
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 26px 30px;
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.75;
    }

    .stat-strip {
        display: flex;
        flex-direction: column;
        gap: 14px;
        height: 100%;
        justify-content: center;
    }

    .stat-pill {
        background: linear-gradient(135deg, rgba(96,165,250,0.1), rgba(168,85,247,0.1));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 12px 16px;
    }

    .stat-pill-num {
        font-size: 20px;
        font-weight: 800;
        color: #f8fafc;
    }

    .stat-pill-label {
        font-size: 11px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ---------- why choose (row cards) ---------- */
    .row-card {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 3px solid rgba(168,85,247,0.5);
        border-radius: 14px;
        padding: 18px 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .row-card:hover {
        transform: translateX(6px);
        box-shadow: 0 10px 24px rgba(124,58,237,0.22);
        cursor: pointer;
    }

    .row-icon {
        font-size: 22px;
        flex-shrink: 0;
    }

    /* ---------- CTA ---------- */
    .cta-box {
        position: relative;
        background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(37,99,235,0.2));
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 18px;
        padding: 36px;
        text-align: center;
        overflow: hidden;
    }

    .cta-heading {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .cta-text {
        color: #cbd5e1;
        font-size: 15px;
        margin-bottom: 20px;
    }

    /* ---------- buttons (main content) ---------- */
    div.stButton > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6em 1.2em;
        transition: filter 0.2s ease, transform 0.2s ease;
    }

    div.stButton > button:hover {
        filter: brightness(1.12);
        transform: translateY(-2px);
        color: white;
    }

    /* ---------- footer ---------- */
    .footer-title {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .footer-tagline {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 6px;
    }

    .footer-copy {
        text-align: center;
        color: #64748b;
        font-size: 12px;
    }

    footer, #MainMenu {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


def info_card(icon, title, text, color="purple", stagger=False):
    stagger_class = "stagger-down" if stagger else ""
    st.markdown(textwrap.dedent(f"""
    <div class="card {stagger_class}">
        <div class="icon-badge badge-{color}">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-text">{text}</div>
    </div>
    """), unsafe_allow_html=True)


def row_card(icon, title, text):
    st.markdown(textwrap.dedent(f"""
    <div class="row-card">
        <div class="row-icon">{icon}</div>
        <div>
            <div class="card-title" style="margin-bottom:4px;">{title}</div>
            <div class="card-text">{text}</div>
        </div>
    </div>
    """), unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR (same nav implementation as Dashboard.py's render_sidebar)
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; padding:0.6rem 0 1rem 0;">
            <div>
                <div style="font-family:'Manrope','Inter',sans-serif; font-weight:700; font-size:1.5rem; color:#F8FAFC; letter-spacing:-0.01em;">Startup Success Predictor</div>
                <div style="font-size:0.72rem; color:#94A3B8; letter-spacing:0.02em;">Startup Analytics Platform</div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:1.4rem;">
            <span class="version-badge">✓ Machine Learning Model </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.1em; "
        "text-transform:uppercase; color:#94A3B8; margin-bottom:0.6rem;'>Navigation</div>",
        unsafe_allow_html=True
    )

    nav_items = [
        ("🏠", "Home"),
        ("📊", "Dashboard"),
        ("📈", "Analytics"),
        ("🔍", "Explorer"),
        ("🤖", "Prediction"),
        ("ℹ️", "About"),
    ]

    if "active_nav" not in st.session_state:
        st.session_state.active_nav = "Home"

    for icon, label in nav_items:
        is_active = st.session_state.active_nav == label
        if is_active:
            st.markdown(f'<div class="nav-active">{icon} &nbsp;{label}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{icon}   {label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.active_nav = label
                st.rerun()

# --------------------------------------------------
# 🚀 HERO SECTION (heading + tagline left, illustration right)
# --------------------------------------------------

hero_left, hero_right = st.columns([1.05, 1], gap="large")

with hero_left:
    st.markdown('<div class="gradient-title-left">Startup Success Analytics Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-bar-left"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline-left">Turn raw startup data into confident decisions. '
        'Our AI models analyze funding, industry and market signals to predict which '
        'startups are built to last.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="tagline-sub">Explore trends across industries and countries, '
        'run instant success predictions, and uncover the insights investors and '
        'founders actually act on — all in one dashboard.</div>',
        unsafe_allow_html=True
    )
    b1, b2 = st.columns(2)
    with b1:
        st.button("🚀 Get Started", use_container_width=True, key="hero_get_started")
    with b2:
        st.button("📊 Explore Dashboard", use_container_width=True, key="hero_explore_dashboard")

with hero_right:
    components.html("""
    <style>
        html, body { margin:0; padding:0; background:transparent; }
    </style>
    <div style="background:transparent; display:flex; align-items:center; justify-content:center;">
    <svg viewBox="0 0 500 460" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-height:440px;">
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

        <circle cx="260" cy="200" r="220" fill="url(#orbGlow)"/>

        <ellipse cx="260" cy="200" rx="170" ry="60" fill="none" stroke="url(#ringGrad)" stroke-width="1.4" opacity="0.55" transform="rotate(-18 260 200)"/>
        <ellipse cx="260" cy="200" rx="140" ry="140" fill="none" stroke="url(#ringGrad)" stroke-width="1" opacity="0.35"/>
        <ellipse cx="260" cy="200" rx="190" ry="80" fill="none" stroke="url(#ringGrad)" stroke-width="1.2" opacity="0.4" transform="rotate(22 260 200)"/>

        <circle cx="260" cy="200" r="46" fill="url(#coreGrad)" opacity="0.95"/>
        <circle cx="260" cy="200" r="60" fill="none" stroke="#a855f7" stroke-width="1" opacity="0.4"/>

        <g stroke="#60a5fa" stroke-width="1" opacity="0.5">
            <line x1="260" y1="200" x2="120" y2="120"/>
            <line x1="260" y1="200" x2="400" y2="110"/>
            <line x1="260" y1="200" x2="110" y2="270"/>
            <line x1="260" y1="200" x2="410" y2="280"/>
            <line x1="260" y1="200" x2="260" y2="60"/>
        </g>
        <circle cx="120" cy="120" r="7" fill="#22d3ee"/>
        <circle cx="400" cy="110" r="6" fill="#a855f7"/>
        <circle cx="110" cy="270" r="6" fill="#60a5fa"/>
        <circle cx="410" cy="280" r="7" fill="#22d3ee"/>
        <circle cx="260" cy="60" r="5" fill="#a855f7"/>

        <g opacity="0.9">
            <rect x="60" y="360" width="18" height="40" rx="4" fill="#7c3aed"/>
            <rect x="86" y="335" width="18" height="65" rx="4" fill="#2563eb"/>
            <rect x="112" y="305" width="18" height="95" rx="4" fill="#22d3ee"/>
            <rect x="138" y="270" width="18" height="130" rx="4" fill="#a855f7"/>
        </g>
        <polyline points="60,400 86,335 112,305 138,270 175,235" fill="none"
                  stroke="#f8fafc" stroke-width="2" opacity="0.7"/>

        <rect x="330" y="330" width="120" height="80" rx="12" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)"/>
        <polyline points="342,395 362,375 382,385 402,355 420,365 438,340" fill="none"
                  stroke="#22d3ee" stroke-width="2.2"/>
        <circle cx="438" cy="340" r="3.5" fill="#22d3ee"/>

        <circle cx="70" cy="90" r="3" fill="#60a5fa" opacity="0.7"/>
        <circle cx="440" cy="70" r="2.5" fill="#a855f7" opacity="0.7"/>
        <circle cx="470" cy="220" r="2" fill="#22d3ee" opacity="0.6"/>
        <circle cx="40" cy="240" r="2.5" fill="#7c3aed" opacity="0.6"/>
    </svg>
    </div>
    """, height=440)

st.write("")
st.write("")

# --------------------------------------------------
# 📖 PLATFORM OVERVIEW
# --------------------------------------------------

st.markdown('<div class="section-heading">📖 Platform Overview</div>', unsafe_allow_html=True)

ov_l, ov_r = st.columns([2, 1])

with ov_l:
    st.markdown(textwrap.dedent("""
    <div class="overview-box">
    The Startup Success Analytics Platform serves as a comprehensive decision-support
    system for the startup ecosystem. Leveraging machine learning and business
    intelligence, it provides predictive insights, interactive visualizations, and
    performance evaluation tools to help entrepreneurs, investors, and researchers
    make informed, data-driven decisions with confidence.
    </div>
    """), unsafe_allow_html=True)

with ov_r:
    st.markdown(textwrap.dedent("""
    <div class="stat-strip">
        <div class="stat-pill"><div class="stat-pill-num">AI Predictions</div><div class="stat-pill-label">Machine Learning Powered</div></div>
        <div class="stat-pill"><div class="stat-pill-num">92%</div><div class="stat-pill-label">Model accuracy</div></div>
        <div class="stat-pill"><div class="stat-pill-num">Real-Time Analytics</div><div class="stat-pill-label">Live Startup Insights</div></div>
    </div>
    """), unsafe_allow_html=True)

st.write("")
st.write("")

# --------------------------------------------------
# ⭐ KEY BENEFITS (staggered / zigzag layout)
# --------------------------------------------------

st.markdown('<div class="section-heading">⭐ Key Benefits</div>', unsafe_allow_html=True)

kb1, kb2, kb3, kb4 = st.columns(4)
with kb1:
    info_card("🤖", "AI-Powered Predictions", "Machine Learning models estimate a startup's probability of success.", color="purple")
with kb2:
    info_card("📊", "Data-Driven Decisions", "Make choices backed by real startup performance data, not guesswork.", color="blue", stagger=True)
with kb3:
    info_card("📈", "Interactive Analytics", "Explore funding, industries and countries through live dashboards.", color="teal")
with kb4:
    info_card("💡", "Actionable Insights", "Turn raw data into clear, business-ready recommendations.", color="coral", stagger=True)

st.write("")
st.write("")

# --------------------------------------------------
# 💡 WHY CHOOSE THIS PLATFORM (alternating row cards)
# --------------------------------------------------

st.markdown('<div class="section-heading">💡 Why Choose This Platform</div>', unsafe_allow_html=True)

wc1, wc2 = st.columns(2)
with wc1:
    row_card("🎯", "Accurate Predictions", "Built on trained ML models for reliable success estimates.")
with wc2:
    row_card("📊", "Interactive Dashboards", "Visualize trends and KPIs without digging through raw data.")

st.write("")

wc3, wc4 = st.columns(2)
with wc3:
    row_card("🧠", "Easy to Understand", "Insights presented clearly, no data science background needed.")
with wc4:
    row_card("⚡", "Fast & Intuitive", "A smooth experience that gets you to answers quickly.")

st.write("")
st.write("")

# --------------------------------------------------
# 🚀 CALL TO ACTION
# --------------------------------------------------

st.markdown("""
<div class="cta-box">
    <div class="cta-heading">🚀 Ready to Explore Startup Analytics?</div>
    <div class="cta-text">Dive into the dashboard or run a prediction to see the platform in action.</div>
</div>
""", unsafe_allow_html=True)

cta_l, cta_c, cta_r = st.columns([1, 1, 1])
with cta_c:
    c1, c2 = st.columns(2)
    with c1:
        st.button("🤖 Start Prediction", use_container_width=True, key="cta_start_prediction")
    with c2:
        st.button("📊 Explore Dashboard", use_container_width=True, key="cta_explore_dashboard_2")

st.write("")
st.write("")

# --------------------------------------------------
# 📄 FOOTER
# --------------------------------------------------

st.markdown("---")
st.markdown('<div class="footer-title">🚀 Startup Success Analytics Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-tagline">AI Powered Startup Prediction & Business Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-copy">© 2026 Startup Success Analytics Platform · All Rights Reserved</div>', unsafe_allow_html=True)