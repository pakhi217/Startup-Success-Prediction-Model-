import time
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_html(html: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in html.strip("\n").splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

st.set_page_config(
    page_title="Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOR_BG = "#0B1120"
COLOR_CARD = "#1E293B"
COLOR_PRIMARY = "#38BDF8"
COLOR_PURPLE = "#A855F7"
COLOR_MINT = "#2DD4BF"
COLOR_TEXT = "#F8FAFC"
COLOR_MUTED = "#94A3B8"
COLOR_DANGER = "#F87171"

CHART_COLORWAY = [COLOR_PRIMARY, COLOR_PURPLE, COLOR_MINT, "#F472B6", "#FACC15", "#818CF8"]
COUNTRY_ISO3 = {
    "United States": "USA", "USA": "USA", "US": "USA", "India": "IND",
    "United Kingdom": "GBR", "UK": "GBR", "Germany": "DEU", "Canada": "CAN",
    "Singapore": "SGP", "France": "FRA", "Israel": "ISR", "Brazil": "BRA",
    "Australia": "AUS", "China": "CHN", "Spain": "ESP", "Netherlands": "NLD",
    "Ireland": "IRL", "Sweden": "SWE", "Russia": "RUS", "South Korea": "KOR",
    "Italy": "ITA", "Japan": "JPN", "Switzerland": "CHE", "Chile": "CHL",
}
import re as _re
_ISO3_PATTERN = _re.compile(r"^[A-Z]{3}$")

def inject_custom_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

        html,
        body,
        [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}
        .stApp {{
    background:
        radial-gradient(circle at 12% 15%, rgba(124,58,237,0.14), transparent 38%),
        radial-gradient(circle at 88% 8%, rgba(37,99,235,0.14), transparent 38%),
        radial-gradient(circle at 50% 95%, rgba(34,211,238,0.08), transparent 40%),
        #0a0e1a;
}}
        @keyframes auroraDrift {{
            0% {{
                background-position: 0% 0%;
            }}
            50% {{
                background-position: 100% 60%;
            }}
            100% {{
                background-position: 0% 0%;
            }}
        }}
        @keyframes fadeSlideUp {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        .block-container {{
            max-width: 1440px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
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

    .hero-section {{

        display:grid;
        grid-template-columns: 1.2fr 1fr;
        align-items:center;
        gap:40px;
        min-height:520px;
        margin-bottom:0px;
        animation:fadeSlideUp .8s ease;
    }}
    .hero-left {{
        display:flex;
        flex-direction:column;
    }}
    .hero-right {{
        display:flex;
        justify-content:center;
        align-items:center;
        position:relative;
    }}  
    .hero-badge {{
    display:inline-block;
    width:fit-content;
    padding:8px 16px;
    border-radius:999px;
    background:rgba(124,58,237,.15);
    border:1px solid rgba(124,58,237,.35);
    color:#B794F4;
    font-size:14px;
    font-weight:600;
    margin-bottom:20px;

}}
.hero-title {{
    font-size:70px;
    line-height:1;
    font-weight:800;
    color:white;
    letter-spacing:-2px;
    margin-bottom:22px;
}}
.hero-title span {{
    background:linear-gradient(
        90deg,
        #7C3AED,
        #3B82F6
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;

}}
.hero-subtitle {{
    font-size:20px;
    line-height:1.9;
    color:#AAB3D3;
    max-width:620px;
    margin-bottom:28px;
}}

.section-header{{
    display:flex;
    align-items:flex-start;
    gap:16px;
    margin-top:10px;
    margin-bottom:35px;
}}
.section-text h2{{
    margin:0;
     font-size:36px;
        font-weight:800;
        color:white;
        margin-bottom:2px;
         white-space: nowrap;
}}
.section-text p{{
    margin-top:4px;
    color:#A7B0C5;
}}
.section-line{{
    width:6px;
    height:44px;
    border-radius:999px;
    background:linear-gradient(
        180deg,
        #7C3AED,
        #3B82F6 );
}}
.section-content{{
    display: flex;
    flex-direction: column;
}}
.section-title{{
    font-size:36px;
    font-weight:800;
    color:white;
    margin-bottom:4px;
     white-space: nowrap;
}}
.section-subtitle{{
    color:#94A3B8;
    font-size:17px;
}}
.widget-container {{
    margin-top:35px;

}}
.widget-card {{
    width:225px;
    padding:18px;
    border-radius:22px;
    position:relative;
    overflow:hidden;
    background:linear-gradient(
        180deg,
        rgba(255,255,255,.06),
        rgba(255,255,255,.03) );
    border:1px solid rgba(255,255,255,.08);
    backdrop-filter:blur(18px);
    transition:.35s;
}}
.widget-card::before {{
    content:"";
    position:absolute;
    top:-70px;
    right:-50px;
    width:140px;
    height:140px;
    border-radius:50%;
    background:rgba(124,58,237,.18);
    filter:blur(60px);
}}
.widget-card:hover {{
    transform:translateY(-10px);
    border-color:rgba(124,58,237,.45);
    box-shadow:
        0 0 50px rgba(124,58,237,.18);
}}
.widget-top {{
    display:flex;
    justify-content:space-between;
    align-items:center;
   margin-bottom:18px;
}}
.widget-icon {{
    width:46px;
height:46px;
border-radius:14px;
font-size:18px;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(
        135deg,
        rgba(124,58,237,.25),
        rgba(59,130,246,.22) );
}}
.widget-footer {{
    margin-top:10px;
    color:#A78BFA;
    font-size:13px;
    font-weight:600;
    transition:.3s;
}}
.widget-card:hover .widget-footer {{
    color:white;
    letter-spacing:.5px;
}}
.widget-status {{
    padding:5px 10px;
    border-radius:999px;
    font-size:11px;
    font-weight:700;
    color:#4ADE80;
    background:rgba(74,222,128,.12);
}}
.widget-value {{
    font-size:38px;
    font-weight:800;
    color:white;
}}
.widget-title {{
    margin-top:4px;
    font-size:16px;
    font-weight:700;
    color:white;
}}
.widget-footer {{
margin-top:10px;
font-size:13px;
    color:#9CA3AF;
}}
.card-two .widget-status {{
    color:#60A5FA;
    background:rgba(96,165,250,.12);
}}
.floating-card {{
    position:absolute;
    transition:.35s;
    z-index:1;
}}
.floating-card:hover {{
    z-index:100;
}}
.card-one {{
    top:-100px;
    left:100px;
}}
.card-two {{
    top:0px;
    left:230px;
}}
.chart-card {{
        background:linear-gradient(
            180deg,
            rgba(255,255,255,.05),
            rgba(255,255,255,.025)
        );
        border:1px solid rgba(255,255,255,.08);
        border-radius:28px;
        padding:28px;
        backdrop-filter:blur(18px);
        transition:.35s;
        margin-bottom:25px;
}}
.chart-card:hover {{
    border-color:rgba(124,58,237,.30);
    box-shadow:
        0 18px 40px rgba(124,58,237,.10);
}}
.chart-title {{
    font-size:24px;
    font-weight:700;
    color:white;
    margin-bottom:8px;
}}
.chart-description {{
    font-size:15px;
    color:#94A3B8;
    margin-bottom:25px;
}}
.chart-header{{
    display:flex;
    align-items:center;
    gap:18px;
    padding:10px 16px;
    margin-bottom:16px;
    background:rgba(255,255,255,.05);
    border:1px solid rgba(255,255,255,.08);
    border-radius:20px;
    backdrop-filter:blur(18px);
    transition:all .35s ease;
    box-shadow:
        0 8px 30px rgba(0,0,0,.18);
}}
.chart-header:hover{{
    transform:translateY(-5px);
    border-color:rgba(255,255,255,.20);
    box-shadow:
        0 15px 35px rgba(0,0,0,.30),
        0 0 25px rgba(168,85,247,.18);
}}
.chart-icon{{
    width:42px;
    height:42px;
    font-size:20px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(
        135deg,
        rgba(192,132,252,.35),
        rgba(165,180,252,.18)
    );
    border:1px solid rgba(255,255,255,.12);
    backdrop-filter:blur(20px);
    transition:.35s;
}}
.chart-header:hover .chart-icon{{
    transform:
        rotate(-6deg)
        scale(1.08);
    box-shadow:
        0 0 25px rgba(192,132,252,.30);
}}
.chart-title{{
    font-size:26px;
    font-weight:700;
    color:white;
    margin-bottom:4px;
}}
.chart-subtitle{{
    color:#B6BDD2;
    font-size:13px;
    opacity:.75;
    line-height:1.5;
}}
@keyframes floatCard{{
    0%{{
        transform:translateY(0px);
    }}
    50%{{
        transform:translateY(-3px);
    }}
    100%{{
        transform:translateY(0px);
    }}
}}
.chart-header{{
    animation:floatCard 5s ease-in-out infinite;
}}
.insight-card{{
    width:100%;
    box-sizing:border-box;
    background:rgba(255,255,255,.05);
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.08);
    border-radius:22px;
    padding:24px;
    min-height:220px;
    transition:.35s;
    margin-bottom:20px;
}}
.insight-card:hover{{
    transform:translateY(-6px);
    border-color:#7C6CFF;
    box-shadow:0 0 30px rgba(124,108,255,.25);
}}
.insight-icon{{
    font-size:34px;
    margin-bottom:15px;
}}
.insight-title{{
    font-size:22px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}}
.insight-text{{
    color:#C9D1E8;
    line-height:1.8;
    font-size:15px;
}}
.sidebar{{
    position:fixed;
    left:0;
    top:0;
    width:250px;
    height:100vh;
    background:#0F172A;
    padding:30px 22px;
    border-right:1px solid rgba(255,255,255,.08);
    z-index:9999;
    overflow-y:auto;
}}
.sidebar-title{{
    font-size:30px;
    font-weight:700;
    color:white;
    margin-bottom:10px;
}}
.sidebar-subtitle{{
    color:#8B93A7;
    font-size:13px;
    margin-bottom:35px;
    letter-spacing:1px;
}}
.sidebar-button{{
    display:block;
    width:100%;
    padding:16px 20px;
    margin-bottom:18px;
    background:#1B2438;
    border-radius:18px;
    color:white;
    text-decoration:none;
    font-size:19px;
    transition:.25s;
    box-sizing:border-box;
}}
.sidebar-button:hover{{
    background:#6D4AFF;
    transform:translateX(6px);
}}
.main .block-container{{
    margin-left:250px;
    max-width:calc(100% - 270px);
    padding-left:3rem;
    padding-right:3rem;
}}
.page-wrapper{{
    margin-left:280px;
    padding-right:30px;
}}
.menu-button{{
    position:fixed;
    top:25px;
    left:25px;
    width:58px;
    height:58px;
    border-radius:18px;
    background:linear-gradient(135deg,#6D4AFF,#8B5CF6);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:28px;
    color:white;
    cursor:pointer;
    box-shadow:0 8px 25px rgba(109,74,255,.45);
    z-index:99999;
    transition:.3s;
}}
.menu-button:hover{{
    transform:scale(1.08);
    box-shadow:0 12px 35px rgba(109,74,255,.7);
}}
.sidebar{{
    position:fixed;
    top:0;
    left:-300px;
    width:280px;
    height:100vh;
    background:#0F172A;
    border-right:1px solid rgba(255,255,255,.08);
    padding:90px 25px 30px;
    box-shadow:10px 0 30px rgba(0,0,0,.4);
    transition:.35s ease;
    z-index:99998;
}}
.sidebar.show{{
    left:0;
}}
.sidebar-title{{
    font-size:30px;
    font-weight:700;
    color:white;
    margin-bottom:12px;
}}
.sidebar-subtitle{{
    color:#8B93A7;
    font-size:13px;
    letter-spacing:1px;
    margin-bottom:35px;
}}
.sidebar-button{{
    display:block;
    padding:16px 20px;
    margin-bottom:16px;
    border-radius:16px;
    background:#182235;
    color:white;
    text-decoration:none;
    font-size:18px;
    transition:.25s;
}}
.sidebar-button:hover{{
    background:#6D4AFF;
    transform:translateX(6px);
}}

section[data-testid="stSidebar"] {{
    background-color: #0d1220;
    border-right: 1px solid rgba(255,255,255,0.06);
}}

section[data-testid="stSidebar"] div.stButton > button {{
    background: #10192b !important;
    color: #cbd5e1 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 0.6em 1em !important;
    justify-content: flex-start !important;
    text-align: left !important;
    box-shadow: none !important;
}}

section[data-testid="stSidebar"] div.stButton > button:hover {{
    background: #16213a !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: #f8fafc !important;
}}
        </style>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.markdown("### 🚀 Startup Analytics")
    st.caption("NAVIGATION")
    if st.button("🏠  Home", use_container_width=True):
        st.switch_page("pages/Home.py")
    if st.button("📊  Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
    if st.button("📈  Analytics", use_container_width=True):
        st.switch_page("pages/Analytics.py")
    if st.button("🌍  Explorer", use_container_width=True):
        st.switch_page("pages/Explorer.py")
    if st.button("🎯  Prediction", use_container_width=True):
        st.switch_page("pages/Prediction.py")
    if st.button("ℹ️  About", use_container_width=True):
        st.switch_page("pages/About.py")

    st.markdown("---")
    st.caption("Version 1.0")

st.markdown("""
<style>

.nav-btn{
    background:#182238;
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:16px;
    margin-bottom:14px;
    color:white;
    font-size:18px;
    font-weight:600;
    text-align:left;
    cursor:pointer;
    transition:.25s;
}
.nav-btn:hover{
    background:#6C4CF6;
    transform:translateX(6px);
    box-shadow:0 0 20px rgba(108,76,246,.45);
}
.sidebar-title{
    font-size:34px;
    font-weight:800;
    color:white;
}
.sidebar-small{
    color:#888;
    letter-spacing:2px;
    margin-top:25px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

inject_custom_css()

DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "cleaned"
    / "clean_startups.csv"
)

df = pd.read_csv(DATA_PATH)
total_startups = len(df)
total_countries = df["country"].nunique()

if total_startups >= 1000:
    startup_display = f"{total_startups / 1000:.1f}K"
else:
    startup_display = str(total_startups)

industry_counts = (
    df["industry"]
    .value_counts()
    .head(8)
    .sort_values()
)

industry_counts.index = industry_counts.index.str.replace("|", "<br>", regex=False)
industry_fig = px.bar(
    x=industry_counts.values,
    y=industry_counts.index,
    orientation="h",
    template="plotly_dark"
)
industry_fig.update_traces(
    marker_color="#5A447F",
    marker_line_width=0
)
industry_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color=COLOR_TEXT,
        family="Inter"
    ),
    margin=dict(
        l=260,
        r=20,
        t=20,
        b=20
    ),
    height=380,
    xaxis_title="Number of Startups",
    yaxis_title="",
    showlegend=False
)
country_counts = (
    df["country"]
    .value_counts()
    .head(8)
    .sort_values()
)
country_fig = px.bar(
    x=country_counts.values,
    y=country_counts.index,
    orientation="h",
    template="plotly_dark"
)
country_fig.update_traces(
    marker_color="#43819C",
    marker_line_width=0,
    width=0.7
)
country_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color=COLOR_TEXT,
        family="Inter"
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),
    height=380,
    xaxis_title="Number of Startups",
    yaxis_title="",
    showlegend=False
)
country_fig.update_xaxes(
    showgrid=True,
    gridcolor="rgba(255,255,255,.08)",
    zeroline=False
)
country_fig.update_yaxes(
    showgrid=False,
    zeroline=False
)
def widget_html(icon, value, title, status, footer):
    return f"""
    <div class="widget-card">
        <div class="widget-top">
            <div class="widget-icon">
                {icon}
            </div>
            <div class="widget-status">
                {status}
            </div>
        </div>
        <div class="widget-value">
            {value}
        </div>
        <div class="widget-title">
            {title}
        </div>
        <div class="widget-footer">
            Explore →
        </div>
    </div>
    """

def chart_header(title, subtitle):
    return f"""
    <div class="chart-header">
        <div class="chart-icon">
            {title.split()[0]}
        </div>
        <div class="chart-text">
            <div class="chart-title">
                {" ".join(title.split()[1:])}
            </div>
            <div class="chart-subtitle">
                {subtitle}
            </div>
        </div>
    </div>
    """
render_html(f"""
<div class="hero-section">
    <div class="hero-left">
        <div class="hero-badge">
            Startup Analytics
        </div>
        <div class="hero-title">
            Analytics<br>
            <span>Dashboard</span>
        </div>
        <div class="hero-subtitle">
            Explore startup funding trends, regional growth,
            industry insights and business performance
            through interactive visualizations.
        </div>
        <div class="hero-divider"></div>
    </div>
    <div class="hero-right">
        <div class="floating-card card-one">
            {widget_html("🚀",startup_display,"Startups","● LIVE","Updated Today")}
        </div>
        <div class="floating-card card-two">
            {widget_html("🌍",total_countries,"Countries","GLOBAL","Across Dataset")}
        </div>
    </div>
</div>
""")

render_html("""
<div class="section-header">
    <div class="section-line"></div>
    <div>
        <div class="section-title">
           📊 Ecosystem Overview
        </div>
        <div class="section-subtitle">
           Explore the structure and distribution of the global startup ecosystem.
        </div>
    </div>
</div>
""")

col1, col2 = st.columns(2, gap="large")
with col1:
    render_html(
        chart_header(
            "🌍 Top Startup Countries",
            "Top countries by startup count."
        )
    )
    st.plotly_chart(
        country_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    render_html("</div>")

with col2:
    render_html(
        chart_header(
            "🏭 Industry Distribution",
            "Number of startups across different industries."
        )
    )
    st.plotly_chart(
        industry_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    render_html("</div>")

status_counts = (
    df["status"]
    .value_counts()
)
status_fig = px.pie(
    values=status_counts.values,
    names=status_counts.index,
    hole=0.65,
    template="plotly_dark"
)
status_fig.update_traces(
    textinfo="none",
    textfont_size=14,
    hovertemplate="<b>%{label}</b><br>%{value} startups<extra></extra>",
    marker=dict(
        colors=[
            "#A5B4FC",
            "#6C7AC2",
            "#4FA795",
            "#8E456D"
        ],
        line=dict(
            color="rgba(255,255,255,0.06)",
            width=1
        )
    )
)
status_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color=COLOR_TEXT,
        family="Inter"
    ),
    height=380,
    legend=dict(
        orientation="h",
        y=-0.15,
        x=0.15
    ),
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=40
    )
)

col3, col4 = st.columns(2, gap="large")
with col3:
    render_html(
        chart_header(
            "👩‍💻 Startup Status",
            "Distribution of startup lifecycle stages."
        )
    )
    st.plotly_chart(
        status_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col4:
    render_html(
        chart_header(
            "📊 Funding Rounds",
            "Distribution of startups by the number of funding rounds."
        )
    )
    round_counts = (
        df["funding_rounds"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
        .head(8)
    )
    round_fig = px.bar(
        x=round_counts.index.astype(str),
        y=round_counts.values,
        template="plotly_dark",
        labels={
            "x": "Funding Rounds",
            "y": "Number of Startups"
        }
    )
    round_fig.update_traces(
        marker_color="#7C89CA",
        hovertemplate="<b>%{x} Funding Rounds</b><br>%{y} Startups<extra></extra>"
    )
    round_fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False,
        xaxis=dict(
            title="Funding Rounds",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Number of Startups",
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        )
    )
    st.plotly_chart(
        round_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    st.markdown("<br>", unsafe_allow_html=True)

render_html("""

    <div class="section-header">
     <div class="section-line"></div>
    

    <div class="section-text">

        <h2>📈 Business Insights</h2>

        <p>
            Advanced analysis of startup growth, funding, and investment trends.
        </p>

    </div>

</div>
""")

from datetime import datetime

df["founded_date"] = pd.to_datetime(df["founded_date"], errors="coerce")

current_year = datetime.now().year
df["company_age"] = current_year - df["founded_date"].dt.year

df = df[
    (df["company_age"] >= 0) &
    (df["company_age"] <= 100)
]

col5, col6 = st.columns(2, gap="large")

with col5:

    render_html(
        chart_header(
            "📈 Company Age",
            "Funding rounds across startups."
        )
    )

    age_fig = px.histogram(
        df,
        x="company_age",
        nbins=20,
        template="plotly_dark"
    )
    age_fig.update_traces(

        marker_color="#358E7C",

        marker_line_width=0,

        hovertemplate=
        "<b>%{x} years</b><br>"
        "%{y} startups<extra></extra>"

    )
    mean_age = df["company_age"].mean()

    age_fig.add_vline(
        x=mean_age,

        line_dash="dash",

        line_color="#7F2C5A",

        annotation_text=f"Average: {mean_age:.1f} yrs",

        annotation_position="top"
    )
    age_fig.update_layout(

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=10
        ),

        xaxis_title="Company Age (Years)",

        yaxis_title="Number of Startups",

        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,.08)",
            zeroline=False
        ),

        showlegend=False
    )
    st.plotly_chart(
        age_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col6:

    render_html(
        chart_header(
            "💰 Funding vs Rounds",
            "Relationship between funding rounds and total funding."
        )
    )
    funding_fig = px.scatter(
        df,
        x="funding_rounds",
        y="total_funding",
        color="status",
        size="total_funding",
        hover_data={
            "country": True,
            "industry": True,
            "company_age": True,
            "funding_rounds": False,
            "total_funding": False
        },
        color_discrete_map={
            "operating": "#72B0A4",
            "acquired": "#6F6695",
            "closed": "#9D915D",
            "ipo": "#A06988"
        },
        size_max=22,
        template="plotly_dark"
    )
    funding_fig.update_traces(

        marker=dict(
            opacity=0.65,
            line=dict(width=0)
        ),

        hovertemplate=
        "<b>%{fullData.name}</b><br><br>"
        "💰 Funding: $%{y:,.0f}<br>"
        "🔁 Funding Rounds: %{x}<br>"
        "🌍 Country: %{customdata[0]}<br>"
        "🏭 Industry: %{customdata[1]}<br>"
        "📈 Company Age: %{customdata[2]} years"
        "<extra></extra>"
    )
    funding_fig.update_yaxes(
        type="log"
    )
    funding_fig.update_layout(

        height=420,
        legend_title_text="",
        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        showlegend=True,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)"
        ),

        xaxis=dict(
            title="Funding Rounds",
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title="Total Funding (Log Scale)",
            gridcolor="rgba(255,255,255,.08)",
            zeroline=False
        )
    )

    st.plotly_chart(
        funding_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

country_mapping = {
    "USA": "United States",
    "GBR": "United Kingdom",
    "IND": "India",
    "CHN": "China",
    "ARE": "United Arab Emirates",
    "CAN": "Canada",
    "FRA": "France",
    "DEU": "Germany",
    "ISR": "Israel",
    "TWN": "Taiwan",
    "BMU": "Bermuda",
    "MUS": "Mauritius",
    "TGO": "Togo",
    "GRD": "Grenada",
    "TAN": "Tanzania",
    "MAF": "Saint Martin"
}
df["country_name"] = df["country"].map(country_mapping)

col7, col8 = st.columns(2, gap="large")
country_funding = (
   df.groupby("country_name")["total_funding"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
)

with col7:

    render_html(
        chart_header(
            "🌍 Funding by Country",
            "Countries with the highest average startup funding."
        )
    )
    country_fig = px.bar(
        x=country_funding.values,
        y=country_funding.index,
        orientation="h",
        template="plotly_dark"
    )
    country_fig.update_traces(

        marker=dict(

            color=country_funding.values,

            colorscale=[
                "#85B1B6",
                "#59889E",
                "#786F9D"
            ],

            line=dict(width=0)

        ),

        hovertemplate=
        "<b>%{y}</b><br>"
        "Average Funding: $%{x:,.0f}"
        "<extra></extra>"
    )
    country_fig.update_layout(

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        showlegend=False,

        xaxis=dict(

            title="Average Funding",

            showgrid=False,

            zeroline=False,

            tickprefix="$",

            tickformat=".2s"
        ),

        yaxis=dict(

            title="",

            gridcolor="rgba(255,255,255,.08)"
        )
    )
    st.plotly_chart(
        country_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )
    country_stats = (
    df.groupby("country")
      .agg(
          avg_funding=("total_funding", "mean"),
          startups=("country", "count")
      )
    )

    country_stats = country_stats[
        country_stats["startups"] >= 20
    ]

    country_stats = country_stats.sort_values(
        "avg_funding",
        ascending=False
    ).head(10)
    x = country_stats["avg_funding"]
    y = country_stats.index

industry_stats = (
    df.groupby("industry")
      .agg(
          avg_funding=("total_funding", "mean"),
          startups=("industry", "count")
      )
)

industry_stats = (
    industry_stats[industry_stats["startups"] >= 20]
    .sort_values("avg_funding", ascending=False)
    .head(10)
)
with col8:

    render_html(
        chart_header(
            "🏭 Funding by Industry",
            "Industries with the highest average funding."
        )
    )
    industry_fig = px.bar(
        x=industry_stats["avg_funding"],
        y=industry_stats.index,
        orientation="h",
        template="plotly_dark"
    )
    industry_fig.update_traces(

        marker=dict(

            color=industry_stats["avg_funding"],

            colorscale=[
                "#BAB1BC",
                "#8973A0",
                "#715EA9"
            ],

            line=dict(width=0)

        ),

        hovertemplate=
        "<b>%{y}</b><br>"
        "Average Funding: $%{x:,.0f}"
        "<extra></extra>"
    )
    industry_fig.update_layout(

        height=420,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        showlegend=False,

        xaxis=dict(
            title="Average Funding",
            showgrid=False,
            zeroline=False,
            tickprefix="$",
            tickformat=".2s"
        ),

        yaxis=dict(
            title="",
            gridcolor="rgba(255,255,255,.08)"
        )
    )

    st.plotly_chart(
        industry_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.markdown("<br>", unsafe_allow_html=True)

funding_time = df[
    ["first_funding_date", "total_funding"]
].copy()

funding_time["first_funding_date"] = pd.to_datetime(
    funding_time["first_funding_date"],
    errors="coerce"
)

funding_time = funding_time.dropna(
    subset=["first_funding_date"]
)

funding_time["year"] = funding_time["first_funding_date"].dt.year

funding_time = funding_time[
    (funding_time["year"] >= 1990) &
    (funding_time["year"] <= 2015)
]

yearly_funding = (
    funding_time
    .groupby("year")
    .agg(
        startups=("first_funding_date", "count"),
        total_funding=("total_funding", "sum")
    )
    .reset_index()
)

funding_time_fig = px.area(
    yearly_funding,
    x="year",
    y="startups",
    markers=True
)

funding_time_fig.update_traces(
    line=dict(
        width=3,
        color="#A5B4FC"
    ),
    fillcolor="rgba(165, 180, 252, 0.12)",
    marker=dict(
        size=7,
        color="#A5B4FC"
    ),
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Startups Funded: %{y:,}"
        "<extra></extra>"
    )
)

funding_time_fig.update_layout(
    height=430,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    margin=dict(l=20, r=20, t=25, b=20),

    xaxis_title="Year",
    yaxis_title="Startups Receiving First Funding",

    xaxis=dict(
        showgrid=False,
        dtick=2
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.07)",
        zeroline=False
    ),

    hoverlabel=dict(
        bgcolor="#1B2038",
        bordercolor="#A5B4FC",
        font=dict(
            color="white",
            size=13
        )
    ),

    showlegend=False
)

st.markdown("<br>", unsafe_allow_html=True)

render_html(
    chart_header(
        "📈 Funding Activity Over Time",
        "Number of startups receiving their first funding across different years."
    )
)

st.plotly_chart(
    funding_time_fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.markdown("<br><br>", unsafe_allow_html=True)

render_html("""
<div class="chart-header">
    <div class="chart-icon">🔥</div>

    <div>
        <h3>Industry × Startup Status</h3>
        <p>Explore how startup outcomes vary across major industries.</p>
    </div>
</div>
""")

heatmap_df = df.dropna(subset=["industry", "status"]).copy()

heatmap_df["primary_industry"] = (
    heatmap_df["industry"]
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

top_industries = (
    heatmap_df["primary_industry"]
    .value_counts()
    .head(10)
    .index
)

heatmap_df = heatmap_df[
    heatmap_df["primary_industry"].isin(top_industries)
]

status_matrix = pd.crosstab(
    heatmap_df["primary_industry"],
    heatmap_df["status"]
)

status_matrix = status_matrix.loc[
    status_matrix.sum(axis=1)
    .sort_values(ascending=False)
    .index
]
fig_heatmap = px.imshow(
    status_matrix,
    text_auto=True,
    aspect="auto",

    labels={
        "x": "Startup Status",
        "y": "Industry",
        "color": "Startups"
    },

    color_continuous_scale=[
        [0.0, "#111827"],
        [0.35, "#4338CA"],
        [0.70, "#7C3AED"],
        [1.0, "#A78BFA"]
    ]
)
fig_heatmap.update_layout(
    height=520,

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="#D8DEE9",
        size=13
    ),

    xaxis=dict(
        title=None,
        side="top"
    ),

    yaxis=dict(
        title=None
    ),

    coloraxis_colorbar=dict(
        title="Startups",
        thickness=12
    )
)

fig_heatmap.update_traces(
    hovertemplate=
        "<b>%{y}</b><br>"
        "Status: %{x}<br>"
        "Startups: %{z:,}"
        "<extra></extra>"
)
st.plotly_chart(
    fig_heatmap,
    use_container_width=True,
    config={"displayModeBar": False}
)

render_html("""
<div class="section-header">

    <div class="section-line"></div>

    <div class="section-text">

        <h2>🔍 Startup Explorer</h2>

        <p>
            Filter and explore startups interactively.
        </p>

    </div>

</div>
""")

filter1, filter2, filter3, filter4 = st.columns(4)
with filter1:

    selected_country = st.selectbox(
        "🌍 Country",
        ["All"] + sorted(df["country"].dropna().unique())
    )

with filter2:

    selected_industry = st.selectbox(
        "🏭 Industry",
        ["All"] + sorted(df["industry"].dropna().unique())
    )

with filter3:

    selected_status = st.selectbox(
        "📊 Status",
        ["All"] + sorted(df["status"].dropna().unique())
    )
with filter4:

    selected_funding = st.slider(
        "💰 Minimum Funding",
        float(df["total_funding"].min()),
        float(df["total_funding"].max()),
        float(df["total_funding"].min())
    )
filtered_df = df.copy()
if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ]
if selected_industry != "All":
    filtered_df = filtered_df[
        filtered_df["industry"] == selected_industry
    ]
if selected_industry != "All":
    filtered_df = filtered_df[
        filtered_df["industry"] == selected_industry
    ]
if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]
filtered_df = filtered_df[
    filtered_df["total_funding"] >= selected_funding
]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:

    st.metric(
        "📈 Startups",
        len(filtered_df)
    )
with kpi2:

    st.metric(
        "💰 Avg Funding",
        f"${filtered_df['total_funding'].mean()/1e6:.1f}M"
    )
with kpi3:

    st.metric(
        "🌍 Countries",
        filtered_df["country"].nunique()
    )
with kpi4:

    st.metric(
        "📅 Avg Age",
        f"{filtered_df['company_age'].mean():.1f} yrs"
    )
st.markdown("### 📋 Startup Database")
display_df = filtered_df[
    [
        "industry",
        "country",
        "status",
        "funding_rounds",
        "total_funding",
        "company_age"
    ]
]
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "startup_data.csv",
    "text/csv"
)

st.markdown("<br>", unsafe_allow_html=True)
insight_df = df.copy()

insight_df["total_funding"] = pd.to_numeric(
    insight_df["total_funding"],
    errors="coerce"
)

insight_df["funding_rounds"] = pd.to_numeric(
    insight_df["funding_rounds"],
    errors="coerce"
)

insight_df["company_age"] = pd.to_numeric(
    insight_df["company_age"],
    errors="coerce"
)

insight_df["first_funding_date"] = pd.to_datetime(
    insight_df["first_funding_date"],
    errors="coerce"
)

funding_years = (
    insight_df
    .dropna(subset=["first_funding_date"])
    .assign(
        funding_year=lambda x: x["first_funding_date"].dt.year
    )
)

funding_year_counts = (
    funding_years["funding_year"]
    .value_counts()
    .sort_index()
)

if not funding_year_counts.empty:
    peak_funding_year = int(funding_year_counts.idxmax())
    peak_funding_count = int(funding_year_counts.max())
else:
    peak_funding_year = "N/A"
    peak_funding_count = 0

industry_status = (
    insight_df
    .dropna(subset=["industry", "status"])
    .groupby(["industry", "status"])
    .size()
    .unstack(fill_value=0)
)

if "acquired" in industry_status.columns:
    top_acquired_industry = industry_status["acquired"].idxmax()
    top_acquired_count = int(
        industry_status["acquired"].max()
    )
else:
    top_acquired_industry = "N/A"
    top_acquired_count = 0

funding_analysis = insight_df[
    insight_df["total_funding"].notna()
    & insight_df["funding_rounds"].notna()
    & (insight_df["total_funding"] > 0)
]

if len(funding_analysis) > 1:
    funding_correlation = funding_analysis[
        ["funding_rounds", "total_funding"]
    ].corr().iloc[0, 1]
else:
    funding_correlation = 0

if funding_correlation >= 0.5:
    funding_relationship = "a strong positive relationship"

elif funding_correlation >= 0.2:
    funding_relationship = "a moderate positive relationship"

elif funding_correlation > 0:
    funding_relationship = "a weak positive relationship"

elif funding_correlation <= -0.2:
    funding_relationship = "a negative relationship"

else:
    funding_relationship = "little overall relationship"

status_age = (
    insight_df
    .dropna(subset=["status", "company_age"])
    .groupby("status")["company_age"]
    .mean()
)

if not status_age.empty:
    oldest_status = status_age.idxmax()
    oldest_status_age = status_age.max()
else:
    oldest_status = "N/A"
    oldest_status_age = 0

print("Peak funding year:", peak_funding_year)
print("Peak funding count:", peak_funding_count)

print("Top acquired industry:", top_acquired_industry)
print("Top acquired count:", top_acquired_count)

print("Funding correlation:", funding_correlation)

print("Oldest status:", oldest_status)
print("Oldest status age:", oldest_status_age)

render_html("""
<div class="section-header">

    <div class="section-line"></div>

    <div class="section-text">

        <h2>💡 Key Analytical Insights</h2>

        <p>
            Data-driven insights generated automatically from the dataset.
        </p>

    </div>

</div>
""")

total_startups = len(df)

top_country = df["country"].mode()[0]

top_industry = (
    df["industry"]
    .mode()[0]
    .split("|")[0]
)

avg_funding = df["total_funding"].mean()

avg_age = df["company_age"].mean()

operating_pct = (
    (
        df["status"] == "operating"
    ).mean() * 100
)

left, right = st.columns(2, gap="large")

with left:

    render_html(f"""
    <div class="insight-card">

        <div class="insight-icon">
            💰
        </div>

        <div class="insight-title">
            Funding Momentum
        </div>

        <div class="insight-text">
            Startup funding peaked in
            <b>{peak_funding_year}</b>,
            with
            <b>{peak_funding_count:,}</b>
            startups receiving their first investment.
        </div>

    </div>
    """)

with right:

    render_html(f"""
    <div class="insight-card">

        <div class="insight-icon">
            🏆
        </div>

        <div class="insight-title">
            Industry Performance
        </div>

        <div class="insight-text">
            <b>{top_acquired_industry}</b>
            recorded the highest number of acquisitions
            (<b>{top_acquired_count}</b> startups),
            making it the strongest acquisition sector.
        </div>

    </div>
    """)
      

left2, right2 = st.columns(2, gap="large")

with left2:

    render_html(f"""
    <div class="insight-card">

        <div class="insight-icon">
            📈
        </div>

        <div class="insight-title">
            Investment Behaviour
        </div>

        <div class="insight-text">
            Funding rounds and total funding show
            <b>{funding_relationship}</b>,
            indicating that startups with more funding rounds
            generally raise more capital.
        </div>

    </div>
    """)

with right2:

    render_html(f"""
    <div class="insight-card">

        <div class="insight-icon">
            🏛
        </div>

        <div class="insight-title">
            Startup Lifecycle
        </div>

        <div class="insight-text">
            <b>{oldest_status.upper()}</b>
            startups have the highest average age
            of
            <b>{oldest_status_age:.1f} years</b>.
        </div>

    </div>
    """)