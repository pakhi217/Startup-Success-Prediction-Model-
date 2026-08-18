import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(
    page_title="Startup Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
    """
    <div class="sidebar-brand">
        <div class="sidebar-title">
            🚀 Startup Success<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Predictor
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    if st.button("🏠  Home", use_container_width=True):
        st.switch_page("pages/Home.py")

    if st.button("📊  Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

    if st.button("📈  Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")

    # CURRENT PAGE — Startup Explorer
    st.markdown(
        """
        <div class="sidebar-active">
            🔍&nbsp;&nbsp; Startup Explorer
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🤖  Prediction", use_container_width=True):
        st.switch_page("pages/Prediction.py")

    if st.button("ℹ️  About", use_container_width=True):
        st.switch_page("pages/About.py")


COLOR_BG = "#0B1120"
COLOR_CARD = "#1E293B"
COLOR_PRIMARY = "#38BDF8"
COLOR_PURPLE = "#A855F7"
COLOR_MINT = "#2DD4BF"
COLOR_TEXT = "#F8FAFC"
COLOR_MUTED = "#94A3B8"
COLOR_DANGER = "#F87171"

CHART_COLORWAY = [
    COLOR_PRIMARY,
    COLOR_PURPLE,
    COLOR_MINT,
    "#F472B6",
    "#FACC15",
    "#818CF8"
]


from pathlib import Path

@st.cache_data
def load_startup_data():
    data_path = Path(__file__).parent.parent.parent / "data" / "cleaned" / "clean_startups.csv"
    return pd.read_csv(data_path)


df = load_startup_data()


st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 12% 8%, rgba(56,189,248,0.14), transparent 42%),
            radial-gradient(circle at 88% 5%, rgba(168,85,247,0.16), transparent 48%),
            radial-gradient(circle at 60% 90%, rgba(45,212,191,0.10), transparent 50%),
            radial-gradient(circle at 25% 70%, rgba(56,189,248,0.06), transparent 45%),
            {COLOR_BG};
        background-size: 200% 200%;
        animation: auroraDrift 24s ease-in-out infinite;
        color: {COLOR_TEXT};
    }}

    /* ============================================================
   SIDEBAR NAVIGATION
   ============================================================ */

section[data-testid="stSidebar"] {{
    background: #0B1120 !important;
    border-right: 1px solid rgba(56,189,248,0.10);
}}

section[data-testid="stSidebar"] > div {{
    background: #0B1120 !important;
}}

section[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem !important;
    padding-left: 1.4rem !important;
    padding-right: 1.4rem !important;
}}


/* ---------- BRAND ---------- */

.sidebar-brand {{
    margin-bottom: 2.8rem;
}}

.sidebar-title {{
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 1.65rem;
    line-height: 1.35;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}}

.sidebar-subtitle {{
    margin-top: 0.45rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #94A3B8;
}}


/* ---------- NORMAL BUTTONS ---------- */

section[data-testid="stSidebar"] .stButton {{
    margin-bottom: 1.05rem;
}}

section[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    height: 55px;

    background: #111827 !important;

    color: #F8FAFC !important;

    border: 1px solid rgba(148,163,184,0.10) !important;

    border-radius: 15px !important;

    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 500;

    box-shadow: none !important;

    transition:
        background 0.2s ease,
        border-color 0.2s ease,
        transform 0.2s ease;
}}

section[data-testid="stSidebar"] .stButton > button:hover {{
    background: #172033 !important;

    border-color: rgba(56,189,248,0.35) !important;

    color: #F8FAFC !important;

    transform: translateY(-1px);
}}


/* ---------- ACTIVE PAGE ---------- */

.sidebar-active {{
    width: 100%;
    height: 55px;

    display: flex;
    align-items: center;
    justify-content: center;

    box-sizing: border-box;

    margin-bottom: 1.05rem;

    border-radius: 15px;

    background:
        linear-gradient(
            100deg,
            rgba(56,189,248,0.16),
            rgba(168,85,247,0.16)
        );

    border: 1px solid #38BDF8;

    color: #38BDF8;

    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 700;

    box-shadow:
        inset 0 0 20px rgba(56,189,248,0.03),
        0 0 12px rgba(56,189,248,0.08);
}}

    @keyframes auroraDrift {{
        0% {{ background-position: 0% 0%; }}
        50% {{ background-position: 100% 60%; }}
        100% {{ background-position: 0% 0%; }}
    }}

    @keyframes fadeSlideUp {{
        from {{
            opacity: 0;
            transform: translateY(14px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: 0% 50%; }}
        100% {{ background-position: 200% 50%; }}
    }}

    @keyframes glow {{
        0%, 100% {{
            box-shadow: 0 0 8px rgba(45,212,191,0.45);
        }}
        50% {{
            box-shadow: 0 0 17px rgba(45,212,191,0.9);
        }}
    }}

    .block-container {{
        padding-top: 1.6rem !important;
        padding-bottom: 3rem !important;
        max-width: 1440px;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    div[data-testid="stToolbar"] {{
        visibility: hidden;
    }}

    .hero-eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        color: {COLOR_PRIMARY};
        background: rgba(56,189,248,0.10);
        border: 1px solid rgba(56,189,248,0.25);
        padding: 5px 14px;
        border-radius: 999px;
        margin-bottom: 1rem;
        animation: fadeSlideUp 0.6s ease;
    }}

    .hero-dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: {COLOR_MINT};
        box-shadow: 0 0 8px {COLOR_MINT};
        animation: glow 2.4s ease-in-out infinite;
    }}

    .hero-title {{
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 2.9rem;
        line-height: 1.12;
        font-weight: 700;
        letter-spacing: -0.02em;
        background:
            linear-gradient(
                100deg,
                {COLOR_TEXT} 10%,
                {COLOR_PRIMARY} 45%,
                {COLOR_PURPLE} 70%,
                {COLOR_MINT} 100%
            );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.35rem;
        animation:
            fadeSlideUp 0.7s ease,
            shimmer 8s linear infinite;
    }}

    .hero-subtitle {{
        font-size: 1.05rem;
        color: {COLOR_MUTED};
        font-weight: 400;
        margin-bottom: 1.1rem;
        animation: fadeSlideUp 0.8s ease;
    }}

    .hero-divider {{
        height: 4px;
        width: 140px;
        border-radius: 10px;
        background:
            linear-gradient(
                90deg,
                {COLOR_PRIMARY},
                {COLOR_PURPLE},
                {COLOR_MINT},
                {COLOR_PRIMARY}
            );
        background-size: 300% auto;
        margin-bottom: 1.9rem;
        box-shadow: 0 0 20px rgba(56,189,248,0.55);
        animation: shimmer 4s linear infinite;
    }}

    .ribbon {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 2rem;
        animation: fadeSlideUp 0.9s ease;
    }}

    .ribbon-chip {{
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(30,41,59,0.55);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148,163,184,0.14);
        padding: 7px 15px;
        border-radius: 999px;
        font-size: 0.8rem;
        color: {COLOR_MUTED};
    }}

    .ribbon-chip b {{
        color: {COLOR_TEXT};
    }}

    .section-header {{
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: 1.18rem;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-top: 1.8rem;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .section-header::before {{
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: linear-gradient(
            135deg,
            {COLOR_PRIMARY},
            {COLOR_MINT}
        );
        box-shadow: 0 0 8px rgba(56,189,248,0.7);
    }}

    .section-sub {{
        display: block;
        font-size: 0.78rem;
        color: {COLOR_MUTED};
        margin-left: 15px;
        margin-bottom: 1rem;
    }}

    .filter-card {{
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.78),
                rgba(15,23,42,0.78)
            );
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 1.2rem 1.3rem 0.6rem 1.3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        backdrop-filter: blur(16px);
        margin-bottom: 1.3rem;
    }}

    .filter-label {{
        color: {COLOR_MUTED};
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }}

    div[data-baseweb="select"] > div {{
        background:
            linear-gradient(
                135deg,
                #DFF3FF,
                #C7EDFF
            ) !important;
        border: 1px solid #7DD3FC !important;
        border-radius: 10px !important;
        min-height: 42px;
    }}

    div[data-baseweb="select"] span {{
        color: #0F172A !important;
        font-weight: 500 !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: #0369A1 !important;
    }}

    div[role="listbox"] {{
        background-color: #E8F7FF !important;
        border: 1px solid #7DD3FC !important;
    }}

    div[role="option"] {{
        color: #0F172A !important;
    }}

    div[role="option"]:hover {{
        background-color: #BAE6FD !important;
    }}

    div[role="option"][aria-selected="true"] {{
        background-color: #BAE6FD !important;
        color: #0F172A !important;
    }}

    .search-box input {{
        background: rgba(223,243,255,0.96) !important;
        color: #0F172A !important;
        border: 1px solid #7DD3FC !important;
        border-radius: 10px !important;
    }}

    .search-box label {{
        color: {COLOR_MUTED} !important;
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.4rem;
    }}

    .kpi-card {{
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.76),
                rgba(15,23,42,0.76)
            );
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 17px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 8px 28px rgba(0,0,0,0.25);
        backdrop-filter: blur(15px);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.35);
    }}

    .kpi-label {{
        font-size: 0.72rem;
        color: {COLOR_MUTED};
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 700;
    }}

    .kpi-value {{
        font-family: 'Space Grotesk', sans-serif;
        color: {COLOR_TEXT};
        font-size: 1.55rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }}

    .kpi-icon {{
        float: right;
        font-size: 1.3rem;
    }}

    .chart-card-wrap {{
        padding: 1px;
        border-radius: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(56,189,248,0.35),
                rgba(168,85,247,0.22),
                rgba(45,212,191,0.22)
            );
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }}

    .chart-card-wrap:hover {{
        transform: translateY(-3px);
    }}

    .chart-card {{
        background:
            linear-gradient(
                160deg,
                rgba(30,41,59,0.88),
                rgba(15,23,42,0.88)
            );
        backdrop-filter: blur(18px);
        border-radius: 19px;
        padding: 1.1rem 1.2rem 0.5rem 1.2rem;
        box-shadow: 0 10px 32px rgba(0,0,0,0.32);
    }}

    .chart-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.02rem;
        font-weight: 700;
        color: {COLOR_TEXT};
        margin-bottom: 0.15rem;
    }}

    .chart-sub {{
        font-size: 0.76rem;
        color: {COLOR_MUTED};
        margin-bottom: 0.5rem;
    }}

    .result-card {{
        background:
            linear-gradient(
                135deg,
                rgba(56,189,248,0.07),
                rgba(168,85,247,0.07)
            );
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 15px;
        padding: 0.9rem 1.1rem;
        color: {COLOR_MUTED};
        margin-bottom: 1rem;
    }}

    .result-card strong {{
        color: {COLOR_TEXT};
    }}

    .table-wrap {{
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.88),
                rgba(15,23,42,0.88)
            );
        border: 1px solid rgba(56,189,248,0.22);
        border-radius: 17px;
        padding: 0.5rem;
        box-shadow: 0 10px 32px rgba(0,0,0,0.3);
    }}

    div[data-testid="stDataFrame"] {{
        background: #DFF3FF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 13px !important;
        overflow: hidden;
    }}

    .detail-card {{
        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.78),
                rgba(15,23,42,0.78)
            );
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
        min-height: 86px;
    }}

    .detail-label {{
        color: {COLOR_MUTED};
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-weight: 700;
    }}

    .detail-value {{
        color: {COLOR_TEXT};
        font-size: 1.05rem;
        font-weight: 650;
        margin-top: 0.3rem;
        word-break: break-word;
    }}

    .status-badge {{
        display: inline-block;
        padding: 4px 11px;
        border-radius: 999px;
        background: rgba(45,212,191,0.11);
        border: 1px solid rgba(45,212,191,0.3);
        color: {COLOR_MINT};
        font-size: 0.76rem;
        font-weight: 700;
    }}

    @media (max-width: 900px) {{
        .kpi-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}

        .hero-title {{
            font-size: 2.3rem;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-eyebrow">
        <span class="hero-dot"></span>
        SEARCH · FILTER · EXPLORE
    </div>

    <div class="hero-title">
        Startup Explorer
    </div>

    <div class="hero-subtitle">
        Explore the startup ecosystem through interactive data, filters,
        funding patterns, and geographic insights.
    </div>

    <div class="hero-divider"></div>
    """,
    unsafe_allow_html=True
)


total_startups = len(df)
total_industries = df["industry"].nunique()
total_countries = df["country"].nunique()

ribbon_items = [
    f"📦 <b>{total_startups:,}</b>&nbsp; startup records",
    f"🏭 <b>{total_industries:,}</b>&nbsp; industries",
    f"🌍 <b>{total_countries:,}</b>&nbsp; countries",
    f"💰 <b>{df['funding_rounds'].sum():,.0f}</b>&nbsp; funding rounds"
]

st.markdown(
    '<div class="ribbon">' +
    "".join(
        f'<div class="ribbon-chip">{item}</div>'
        for item in ribbon_items
    ) +
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="section-header">Explore the Dataset</div>
    <span class="section-sub">
        Narrow the ecosystem down using multiple filters and inspect the resulting startup records.
    </span>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="filter-card">', unsafe_allow_html=True)

search_col, industry_col, country_col, status_col = st.columns([1.5, 1, 1, 1])

with search_col:
    st.markdown(
        '<div class="filter-label">Search</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "Search",
        placeholder="Search industry, city, region...",
        label_visibility="collapsed"
    )

with industry_col:
    st.markdown(
        '<div class="filter-label">Industry</div>',
        unsafe_allow_html=True
    )

    industry_options = ["All Industries"] + sorted(
        df["industry"].dropna().astype(str).unique().tolist()
    )

    selected_industry = st.selectbox(
        "Industry",
        industry_options,
        label_visibility="collapsed"
    )

with country_col:
    st.markdown(
        '<div class="filter-label">Country</div>',
        unsafe_allow_html=True
    )

    country_options = ["All Countries"] + sorted(
        df["country"].dropna().astype(str).unique().tolist()
    )

    selected_country = st.selectbox(
        "Country",
        country_options,
        label_visibility="collapsed"
    )

with status_col:
    st.markdown(
        '<div class="filter-label">Status</div>',
        unsafe_allow_html=True
    )

    status_options = ["All Statuses"] + sorted(
        df["status"].dropna().astype(str).unique().tolist()
    )

    selected_status = st.selectbox(
        "Status",
        status_options,
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)


filtered_df = df.copy()


if search_text:
    search_columns = [
        "industry",
        "country",
        "region",
        "city",
        "status"
    ]

    search_mask = pd.Series(False, index=filtered_df.index)

    for column in search_columns:
        search_mask |= (
            filtered_df[column]
            .fillna("")
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False,
                regex=False
            )
        )

    filtered_df = filtered_df[search_mask]


if selected_industry != "All Industries":
    filtered_df = filtered_df[
        filtered_df["industry"].astype(str) == selected_industry
    ]


if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["country"].astype(str) == selected_country
    ]


if selected_status != "All Statuses":
    filtered_df = filtered_df[
        filtered_df["status"].astype(str) == selected_status
    ]


percentage = (
    len(filtered_df) / len(df) * 100
    if len(df)
    else 0
)


st.markdown(
    f"""
    <div class="result-card">
        Showing <strong>{len(filtered_df):,}</strong>
        startup records
        &nbsp;·&nbsp;
        <strong>{percentage:.1f}%</strong>
        of the complete dataset
    </div>
    """,
    unsafe_allow_html=True
)


kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <span class="kpi-icon">🔎</span>
            <div class="kpi-label">Matching Records</div>
            <div class="kpi-value">{len(filtered_df):,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_cols[1]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <span class="kpi-icon">🏭</span>
            <div class="kpi-label">Industries</div>
            <div class="kpi-value">{filtered_df["industry"].nunique():,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_cols[2]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <span class="kpi-icon">🌍</span>
            <div class="kpi-label">Countries</div>
            <div class="kpi-value">{filtered_df["country"].nunique():,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi_cols[3]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <span class="kpi-icon">💰</span>
            <div class="kpi-label">Funding Rounds</div>
            <div class="kpi-value">{filtered_df["funding_rounds"].sum():,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="section-header">Startup Exploration</div>
    <span class="section-sub">
        Explore the funding history and age profile of the startups currently matching your filters.
    </span>
    """,
    unsafe_allow_html=True
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    rounds_data = (
        filtered_df["funding_rounds"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rounds_data.columns = ["Funding Rounds", "Startups"]

    fig_rounds = px.bar(
        rounds_data,
        x="Funding Rounds",
        y="Startups"
    )

    fig_rounds.update_traces(
        marker_color=COLOR_PRIMARY,
        marker_line_width=0,
        opacity=0.9
    )

    fig_rounds.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=COLOR_TEXT,
            family="Inter, sans-serif"
        ),
        margin=dict(l=5, r=10, t=45, b=10),
        height=350,
        title=dict(
    text="🔄 Funding Round Profile",
    font=dict(
        size=18,
        color="#FFFFFF"
    )
),
        xaxis_title="Funding Rounds",
        yaxis_title="Startup Records",
        xaxis=dict(
            gridcolor="rgba(148,163,184,0.10)",
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,0.10)",
            zeroline=False
        )
    )

    st.markdown(
        '<div class="chart-card-wrap"><div class="chart-card">',
        unsafe_allow_html=True
    )

    st.caption(
        "How many funding rounds the selected startups have completed."
    )

    st.plotly_chart(
        fig_rounds,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '</div></div>',
        unsafe_allow_html=True
    )


with chart_col2:

    founding_data = filtered_df.copy()

    founding_data["founded_date"] = pd.to_datetime(
        founding_data["founded_date"],
        errors="coerce"
    )

    founding_data = founding_data.dropna(
        subset=["founded_date"]
    )

    st.markdown(
        '<div class="chart-card-wrap"><div class="chart-card">',
        unsafe_allow_html=True
    )

    if len(founding_data) > 0:

        founding_data["Founded Year"] = (
            founding_data["founded_date"]
            .dt.year
            .astype(int)
        )

        year_counts = (
            founding_data["Founded Year"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        year_counts.columns = [
            "Founded Year",
            "Startups"
        ]

        fig_founding = px.area(
            year_counts,
            x="Founded Year",
            y="Startups"
        )

        fig_founding.update_traces(
            line_color=COLOR_PURPLE,
            fillcolor="rgba(168,85,247,0.20)"
        )

        fig_founding.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=COLOR_TEXT,
                family="Inter, sans-serif"
            ),
            margin=dict(l=5, r=10, t=45, b=10),
            height=350,
            title=dict(
    text="📅 Startup Founding Timeline",
    font=dict(
        size=18,
        color="#FFFFFF"
    )
),
            xaxis_title="Founded Year",
            yaxis_title="Startup Records",
            xaxis=dict(
                gridcolor="rgba(148,163,184,0.10)",
                zeroline=False
            ),
            yaxis=dict(
                gridcolor="rgba(148,163,184,0.10)",
                zeroline=False
            )
        )

        st.caption(
            "When the startups in your current selection were founded."
        )

        st.plotly_chart(
            fig_founding,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    else:

        st.warning(
            "No valid founding-date information is available for the current selection."
        )

    st.markdown(
        '</div></div>',
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="section-header">Startup Data</div>
    <span class="section-sub">
        Inspect the underlying records returned by your filters.
    </span>
    """,
    unsafe_allow_html=True
)


display_columns = [
    "industry",
    "total_funding",
    "status",
    "country",
    "region",
    "city",
    "funding_rounds",
    "founded_date",
    "first_funding_date",
    "last_funding_date"
]


st.markdown(
    '<div class="table-wrap">',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
    height=480
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="section-header">Record Details</div>
    <span class="section-sub">
        Select a record to inspect its key attributes.
    </span>
    """,
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    selected_index = st.selectbox(
        "Select a startup record",
        filtered_df.index.tolist(),
        format_func=lambda x: f"Startup record #{x + 1}",
        label_visibility="collapsed"
    )

    startup = filtered_df.loc[selected_index]

    detail_cols = st.columns(3)

    with detail_cols[0]:

        st.markdown(
            f"""
            <div class="detail-card">
                <div class="detail-label">Industry</div>
                <div class="detail-value">{startup["industry"]}</div>
            </div>

            <div class="detail-card">
                <div class="detail-label">Country</div>
                <div class="detail-value">{startup["country"]}</div>
            </div>

            <div class="detail-card">
                <div class="detail-label">Region</div>
                <div class="detail-value">{startup["region"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail_cols[1]:

        st.markdown(
            f"""
            <div class="detail-card">
                <div class="detail-label">Status</div>
                <div class="detail-value">
                    <span class="status-badge">{startup["status"]}</span>
                </div>
            </div>

            <div class="detail-card">
                <div class="detail-label">City</div>
                <div class="detail-value">{startup["city"]}</div>
            </div>

            <div class="detail-card">
                <div class="detail-label">Funding Rounds</div>
                <div class="detail-value">{startup["funding_rounds"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail_cols[2]:

        st.markdown(
            f"""
            <div class="detail-card">
                <div class="detail-label">Total Funding</div>
                <div class="detail-value">{startup["total_funding"]}</div>
            </div>

            <div class="detail-card">
                <div class="detail-label">Founded</div>
                <div class="detail-value">{startup["founded_date"]}</div>
            </div>

            <div class="detail-card">
                <div class="detail-label">Last Funding</div>
                <div class="detail-value">{startup["last_funding_date"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.warning("No startup records match the selected filters.")