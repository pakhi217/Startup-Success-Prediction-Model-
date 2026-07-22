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
    page_title="Dashboard",
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
        /* ---------- Premium Font Import ---------- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        /* ---------- Animated Aurora Background ---------- */
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

        @keyframes auroraDrift {{
            0%   {{ background-position: 0% 0%; }}
            50%  {{ background-position: 100% 60%; }}
            100% {{ background-position: 0% 0%; }}
        }}
        @keyframes fadeSlideUp {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes shimmerBorder {{
            0%   {{ background-position: 0% 50%; }}
            100% {{ background-position: 200% 50%; }}
        }}
        @keyframes softPulseGlow {{
            0%, 100% {{ box-shadow: 0 0 8px rgba(45,212,191,0.6); }}
            50%      {{ box-shadow: 0 0 16px rgba(45,212,191,0.95); }}
        }}
        @keyframes skeletonShimmer {{
            0%   {{ background-position: -400px 0; }}
            100% {{ background-position: 400px 0; }}
        }}
        @keyframes rippleEffect {{
            from {{ transform: scale(0); opacity: 0.55; }}
            to   {{ transform: scale(2.6); opacity: 0; }}
        }}

        /* Main block container spacing */
        .block-container {{
            padding-top: 1.6rem !important;
            padding-bottom: 2rem !important;
            max-width: 1440px;
        }}

        /* ---------- Remove Streamlit Chrome ---------- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
        div[data-testid="stToolbar"] {{visibility: hidden; height: 0;}}
        div[data-testid="stDecoration"] {{display: none;}}
        div[data-testid="stStatusWidget"] {{visibility: hidden;}}
        a[href*="streamlit.io"] {{display: none !important;}}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(15,23,42,0.98) 0%, rgba(11,17,32,0.99) 100%);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(148,163,184,0.10);
        }}
        section[data-testid="stSidebar"] .stButton button {{
            width: 100%;
            text-align: left;
            background: rgba(255,255,255,0.02);
            color: {COLOR_TEXT};
            border: 1px solid rgba(148,163,184,0.08);
            border-radius: 12px;
            padding: 0.6rem 1rem;
            margin-bottom: 6px;
            font-weight: 500;
            letter-spacing: 0.01em;
            transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        section[data-testid="stSidebar"] .stButton button::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, rgba(56,189,248,0.18), rgba(168,85,247,0.18));
            opacity: 0;
            transition: opacity 0.28s ease;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            border: 1px solid rgba(56,189,248,0.45);
            color: {COLOR_PRIMARY};
            transform: translateX(5px);
            box-shadow: 0 4px 18px rgba(56,189,248,0.18);
        }}
        section[data-testid="stSidebar"] .stButton button:hover::before {{ opacity: 1; }}
        section[data-testid="stSidebar"] .stButton button:active {{ transform: translateX(5px) scale(0.98); }}

        .nav-active {{
            background: linear-gradient(90deg, rgba(56,189,248,0.16), rgba(168,85,247,0.10)) !important;
            border: 1px solid rgba(56,189,248,0.4) !important;
            border-left: 3px solid {COLOR_PRIMARY} !important;
            border-radius: 10px;
            padding: 0.6rem 1rem 0.6rem 0.85rem;
            margin-bottom: 6px;
            font-weight: 700;
            color: {COLOR_PRIMARY} !important;
            font-size: 0.92rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-item {{
            border-radius: 10px;
            padding: 0.6rem 1rem;
            margin-bottom: 6px;
            font-weight: 500;
            color: {COLOR_MUTED};
            font-size: 0.92rem;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.25s ease;
        }}
        .nav-item:hover {{
            background: rgba(148,163,184,0.06);
            color: {COLOR_TEXT};
        }}

        .version-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            color: {COLOR_MINT};
            background: rgba(45,212,191,0.10);
            border: 1px solid rgba(45,212,191,0.28);
            padding: 3px 10px;
            border-radius: 999px;
        }}
        .online-dot {{
            width: 7px; height: 7px; border-radius: 50%;
            background: {COLOR_MINT};
            display: inline-block;
            animation: softPulseGlow 2.2s ease-in-out infinite;
        }}

        /* ---------- Hero Section ---------- */
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
        .hero-eyebrow .dot {{
            width: 6px; height: 6px; border-radius: 50%;
            background: {COLOR_MINT};
            box-shadow: 0 0 8px {COLOR_MINT};
            animation: softPulseGlow 2.4s ease-in-out infinite;
        }}
        .hero-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .hero-meta {{
            text-align: right;
            font-size: 0.78rem;
            color: {COLOR_MUTED};
            animation: fadeSlideUp 0.7s ease;
        }}
        .hero-meta .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(45,212,191,0.10);
            border: 1px solid rgba(45,212,191,0.3);
            color: {COLOR_MINT};
            font-weight: 700;
            font-size: 0.72rem;
            padding: 4px 11px;
            border-radius: 999px;
            margin-bottom: 6px;
        }}
        .hero-title {{
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: 2.9rem;
            line-height: 1.12;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(100deg, {COLOR_TEXT} 10%, {COLOR_PRIMARY} 45%, {COLOR_PURPLE} 70%, {COLOR_MINT} 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.35rem;
            animation: fadeSlideUp 0.7s ease, shimmerBorder 8s linear infinite;
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
            background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_PURPLE}, {COLOR_MINT}, {COLOR_PRIMARY});
            background-size: 300% auto;
            margin-bottom: 1.4rem;
            box-shadow: 0 0 20px rgba(56,189,248,0.55);
            animation: shimmerBorder 4s linear infinite;
        }}

        /* KPI Ribbon */
        .kpi-ribbon {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 2.2rem;
            animation: fadeSlideUp 0.9s ease;
        }}
        .ribbon-chip {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(30,41,59,0.55);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(148,163,184,0.14);
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            color: {COLOR_MUTED};
            transition: all 0.25s ease;
        }}
        .ribbon-chip:hover {{
            border-color: rgba(56,189,248,0.4);
            color: {COLOR_TEXT};
            transform: translateY(-2px);
        }}
        .ribbon-chip b {{ color: {COLOR_TEXT}; font-weight: 700; }}

        /* ---------- Glass Cards (KPI) w/ Gradient Border ---------- */
        .glass-card-wrap {{
            position: relative;
            border-radius: 20px;
            padding: 1.5px;
            background: linear-gradient(135deg, rgba(56,189,248,0.35), rgba(148,163,184,0.06) 40%, rgba(168,85,247,0.30) 100%);
            height: 100%;
            animation: fadeSlideUp 0.6s ease both;
            transition: background 0.35s ease;
        }}
        .glass-card-wrap:hover {{
            background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_PURPLE} 55%, {COLOR_MINT} 100%);
        }}
        .glass-card {{
            position: relative;
            background: linear-gradient(160deg, rgba(30,41,59,0.78), rgba(15,23,42,0.78));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-radius: 18.5px;
            padding: 1.4rem 1.5rem 0.2rem 1.5rem;
            box-shadow: 0 10px 32px rgba(0,0,0,0.38);
            transition: transform 0.32s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.32s ease;
            overflow: hidden;
        }}
        .glass-card-wrap:hover .glass-card {{
            transform: translateY(-8px) scale(1.015);
            box-shadow: 0 18px 46px rgba(56,189,248,0.22);
        }}
        .kpi-card-footer {{
            background: linear-gradient(160deg, rgba(30,41,59,0.78), rgba(15,23,42,0.78));
            backdrop-filter: blur(18px);
            border-radius: 0 0 18.5px 18.5px;
            padding: 0 1.5rem 1.3rem 1.5rem;
            margin-top: -6px;
        }}
        .kpi-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .kpi-icon {{
            font-size: 1.55rem;
            width: 42px; height: 42px;
            display: flex; align-items: center; justify-content: center;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(168,85,247,0.16));
            filter: drop-shadow(0 0 8px rgba(56,189,248,0.25));
            transition: transform 0.35s ease;
        }}
        .glass-card-wrap:hover .kpi-icon {{ transform: scale(1.12) rotate(-4deg); }}
        .kpi-trend {{
            font-size: 0.74rem;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 999px;
        }}
        .kpi-trend.up {{ background: rgba(45,212,191,0.14); color: {COLOR_MINT}; }}
        .kpi-trend.down {{ background: rgba(248,113,113,0.14); color: {COLOR_DANGER}; }}
        .kpi-label {{
            font-size: 0.76rem;
            font-weight: 700;
            color: {COLOR_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.07em;
            margin: 0.7rem 0 0.15rem 0;
        }}
        .kpi-value {{
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: 2.1rem;
            font-weight: 700;
            color: {COLOR_TEXT};
            margin: 0;
            letter-spacing: -0.01em;
        }}
        .kpi-desc {{
            font-size: 0.79rem;
            color: {COLOR_MUTED};
            margin-top: 0.15rem;
            opacity: 0.85;
        }}

        /* Sparkline tucked into KPI card */
        div[data-testid="stVerticalBlock"] div[data-testid="stPlotlyChart"] {{
            margin-top: -14px;
            margin-bottom: -10px;
        }}

        /* ---------- Section Headers ---------- */
        .section-header {{
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: 1.32rem;
            font-weight: 700;
            color: {COLOR_TEXT};
            margin-top: 2.4rem;
            margin-bottom: 1.1rem;
            padding-left: 0.85rem;
            position: relative;
            display: flex;
            align-items: center;
            animation: fadeSlideUp 0.6s ease both;
        }}
        .section-header::before {{
            content: "";
            position: absolute;
            left: 0; top: 50%;
            transform: translateY(-50%);
            width: 4px; height: 1.4rem;
            border-radius: 10px;
            background: linear-gradient(180deg, {COLOR_PRIMARY}, {COLOR_PURPLE});
            box-shadow: 0 0 10px rgba(56,189,248,0.5);
        }}
        .section-sub {{
            font-size: 0.85rem;
            color: {COLOR_MUTED};
            font-weight: 400;
            margin-left: 0.6rem;
        }}

        /* ---------- Filter Bar ---------- */
        .filter-bar-wrap {{
            position: relative;
            border-radius: 20px;
            padding: 1.5px;
            background: linear-gradient(135deg, rgba(56,189,248,0.28), rgba(168,85,247,0.22));
            margin-bottom: 1.8rem;
            animation: fadeSlideUp 0.6s ease both;
        }}
        .filter-bar {{
            background: linear-gradient(160deg, rgba(30,41,59,0.78), rgba(15,23,42,0.78));
            backdrop-filter: blur(18px);
            border-radius: 18.5px;
            padding: 1.1rem 1.4rem 0.3rem 1.4rem;
        }}
        .filter-label {{
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {COLOR_MUTED};
            margin-bottom: 2px;
        }}
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {{
            background: rgba(255,255,255,0.03) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(148,163,184,0.18) !important;
        }}
        div[data-baseweb="select"]:hover > div {{
            border-color: rgba(56,189,248,0.45) !important;
        }}
        .stTextInput > div > div > input {{
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            border: 1px solid rgba(148,163,184,0.18);
            color: {COLOR_TEXT};
        }}
        div[data-testid="stSlider"] > div > div > div > div {{
            background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_PURPLE});
        }}

        /* ---------- Chart / Plot Containers w/ Gradient Border ---------- */
        .chart-card-wrap {{
            position: relative;
            border-radius: 21px;
            padding: 1.5px;
            background: linear-gradient(135deg, rgba(148,163,184,0.14), rgba(168,85,247,0.22) 55%, rgba(56,189,248,0.20) 100%);
            margin-bottom: 1.5rem;
            animation: fadeSlideUp 0.65s ease both;
            transition: background 0.4s ease, transform 0.35s ease;
        }}
        .chart-card-wrap:hover {{
            background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_PURPLE} 50%, {COLOR_MINT} 100%);
            transform: translateY(-3px);
        }}
        .chart-card {{
            background: linear-gradient(160deg, rgba(30,41,59,0.72), rgba(15,23,42,0.72));
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-radius: 19.5px;
            padding: 1.3rem 1.4rem 0.5rem 1.4rem;
            box-shadow: 0 10px 32px rgba(0,0,0,0.32);
            transition: box-shadow 0.35s ease;
        }}
        .chart-card-wrap:hover .chart-card {{ box-shadow: 0 16px 44px rgba(168,85,247,0.18); }}
        .chart-title {{
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: 1.04rem;
            font-weight: 700;
            color: {COLOR_TEXT};
            margin-bottom: 0.15rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .chart-title::before {{
            content: "";
            width: 7px; height: 7px; border-radius: 50%;
            background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_MINT});
            box-shadow: 0 0 8px rgba(56,189,248,0.7);
        }}
        .chart-sub {{
            font-size: 0.78rem;
            color: {COLOR_MUTED};
            margin-bottom: 0.7rem;
            opacity: 0.9;
        }}

        /* ---------- AI Insights Panel ---------- */
        .insight-card {{
            background: linear-gradient(135deg, rgba(56,189,248,0.07), rgba(168,85,247,0.07));
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 16px;
            padding: 0.95rem 1.1rem;
            margin-bottom: 0.7rem;
            display: flex;
            gap: 12px;
            align-items: flex-start;
            transition: all 0.28s ease;
        }}
        .insight-card:hover {{
            border-color: rgba(56,189,248,0.4);
            transform: translateX(4px);
            background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(168,85,247,0.12));
        }}
        .insight-icon {{ font-size: 1.15rem; margin-top: 1px; }}
        .insight-text {{ font-size: 0.86rem; color: {COLOR_TEXT}; line-height: 1.45; }}
        .insight-text b {{ color: {COLOR_PRIMARY}; }}

        /* ---------- Leaderboard ---------- */
        .leader-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 0.8rem 0.9rem;
            border-radius: 14px;
            margin-bottom: 0.55rem;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(148,163,184,0.10);
            transition: all 0.25s ease;
        }}
        .leader-row:hover {{
            background: rgba(56,189,248,0.06);
            border-color: rgba(56,189,248,0.3);
            transform: translateX(3px);
        }}
        .leader-rank {{
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            width: 30px; height: 30px;
            border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            background: rgba(148,163,184,0.10);
            color: {COLOR_MUTED};
        }}
        .leader-rank.gold {{ background: rgba(250,204,21,0.16); color: #FACC15; }}
        .leader-rank.silver {{ background: rgba(203,213,225,0.16); color: #E2E8F0; }}
        .leader-rank.bronze {{ background: rgba(217,119,6,0.16); color: #F59E0B; }}
        .leader-name {{ font-weight: 600; font-size: 0.88rem; color: {COLOR_TEXT}; }}
        .leader-sub {{ font-size: 0.72rem; color: {COLOR_MUTED}; }}
        .leader-funding {{
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700; font-size: 0.9rem; color: {COLOR_MINT};
            white-space: nowrap;
        }}

        /* ---------- Custom Table ---------- */
        .aurora-table-wrap {{
            position: relative;
            border-radius: 21px;
            padding: 1.5px;
            background: linear-gradient(135deg, rgba(148,163,184,0.14), rgba(56,189,248,0.22));
            animation: fadeSlideUp 0.6s ease both;
        }}
        .aurora-table {{
            background: linear-gradient(160deg, rgba(30,41,59,0.72), rgba(15,23,42,0.72));
            backdrop-filter: blur(18px);
            border-radius: 19.5px;
            padding: 1.2rem 1.3rem;
            overflow-x: auto;
        }}
        table.aurora-html-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.86rem;
        }}
        table.aurora-html-table thead th {{
            text-align: left;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {COLOR_MUTED};
            font-weight: 700;
            padding: 8px 12px;
            border-bottom: 1px solid rgba(148,163,184,0.14);
        }}
        table.aurora-html-table tbody td {{
            padding: 10px 12px;
            color: {COLOR_TEXT};
            border-bottom: 1px solid rgba(148,163,184,0.07);
        }}
        table.aurora-html-table tbody tr {{
            transition: background 0.2s ease;
        }}
        table.aurora-html-table tbody tr:hover {{
            background: rgba(56,189,248,0.06);
        }}

        /* ---------- Buttons (Global, non-sidebar) ---------- */
        .stButton > button {{
            border-radius: 12px;
            border: 1px solid rgba(56,189,248,0.4);
            background: linear-gradient(90deg, rgba(56,189,248,0.15), rgba(168,85,247,0.15));
            color: {COLOR_TEXT};
            font-weight: 600;
            padding: 0.55rem 1.15rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }}
        .stButton > button:hover {{
            border: 1px solid {COLOR_PRIMARY};
            box-shadow: 0 0 20px rgba(56,189,248,0.4);
            transform: translateY(-2px);
        }}
        .stButton > button:active {{ transform: translateY(0) scale(0.97); }}

        /* ---------- Badges (status pills) ---------- */
        .badge-success {{
            background: rgba(45,212,191,0.14);
            color: {COLOR_MINT};
            border: 1px solid rgba(45,212,191,0.35);
            padding: 3px 11px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(45,212,191,0.15);
            display: inline-block;
        }}
        .badge-failed {{
            background: rgba(248,113,113,0.14);
            color: {COLOR_DANGER};
            border: 1px solid rgba(248,113,113,0.35);
            padding: 3px 11px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            box-shadow: 0 0 10px rgba(248,113,113,0.12);
            display: inline-block;
        }}

        /* ---------- Skeleton Loader ---------- */
        .skeleton {{
            background: linear-gradient(90deg, rgba(148,163,184,0.06) 25%, rgba(148,163,184,0.14) 37%, rgba(148,163,184,0.06) 63%);
            background-size: 800px 100%;
            animation: skeletonShimmer 1.4s ease-in-out infinite;
            border-radius: 16px;
        }}

        /* ---------- Scrollbar ---------- */
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-track {{ background: {COLOR_BG}; }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLOR_PRIMARY}, {COLOR_PURPLE});
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: {COLOR_MINT}; }}

        /* ---------- Sidebar Footer ---------- */
        .sidebar-footer {{
            position: fixed;
            bottom: 1.2rem;
            font-size: 0.75rem;
            color: {COLOR_MUTED};
            padding-left: 0.4rem;
        }}

        /* ---------- Responsive tweaks for smaller laptop screens ---------- */
        @media (max-width: 1200px) {{
            .hero-title {{ font-size: 2.3rem; }}
            .kpi-value {{ font-size: 1.7rem; }}
            .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_loading_skeleton():
    
    placeholder = st.empty()
    skeleton_html = """
<div style="display:flex; flex-direction:column; gap:14px; padding-top:10px;">
<div class="skeleton" style="height:36px; width:55%;"></div>
<div class="skeleton" style="height:16px; width:35%;"></div>
<div style="display:flex; gap:14px; margin-top:10px;">
<div class="skeleton" style="height:120px; width:25%;"></div>
<div class="skeleton" style="height:120px; width:25%;"></div>
<div class="skeleton" style="height:120px; width:25%;"></div>
<div class="skeleton" style="height:120px; width:25%;"></div>
</div>
<div class="skeleton" style="height:340px; width:100%; margin-top:10px;"></div>
</div>
"""
    placeholder.markdown(skeleton_html, unsafe_allow_html=True)
    time.sleep(0.55)
    placeholder.empty()



DATA_FILENAME = "clean_startups.csv"


def _resolve_data_path(filename: str = DATA_FILENAME) -> Path:
    
    here = Path(__file__).resolve().parent
    candidates = [
        here / filename,                                   
        Path.cwd() / filename,                              
        here.parent.parent / "data" / "cleaned" / filename,  
        Path.cwd() / "data" / "cleaned" / filename,          
        Path(filename),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return Path(filename)  


def _find_column(columns, keywords, used=None):
    
    used = used or set()
    cols_lower = {c: str(c).lower() for c in columns}
    for kw in keywords:
        for col, low in cols_lower.items():
            if col in used:
                continue
            if kw in low:
                return col
    return None


@st.cache_data
def infer_schema(df: pd.DataFrame) -> dict:
    
    cols = list(df.columns)
    used = set()
    schema = {}

    def assign(key, keywords):
        found = _find_column(cols, keywords, used)
        if found:
            used.add(found)
        schema[key] = found

    assign("company", ["company_name", "startup_name", "org_name", "name"])
    assign("industry", ["industry", "category", "sector", "vertical"])
    assign("status", ["status", "outcome", "state"])
    assign("country", ["country", "nation"])
    assign("region", ["region", "state", "province"])
    assign("city", ["city", "town", "location"])
    assign("funding", ["total_funding", "funding_total", "amount_raised", "total_raised", "raised", "amount", "funding"])
    assign("funding_rounds", ["funding_rounds", "num_rounds", "round_count", "rounds"])
    assign("founded_date", ["founded", "incorporation", "launch_date", "start_date"])
    assign("first_funding_date", ["first_funding", "firstfunding", "seed_date"])
    assign("last_funding_date", ["last_funding", "lastfunding", "latest_funding"])

    return schema


def _is_iso3_series(series: pd.Series) -> bool:
    
    sample = series.dropna().astype(str).head(200)
    if sample.empty:
        return False
    matches = sample.str.match(_ISO3_PATTERN)
    return matches.mean() > 0.9


@st.cache_data
def load_startup_data(filename: str = DATA_FILENAME) -> pd.DataFrame:
    
    path = _resolve_data_path(filename)
    raw = pd.read_csv(path)
    schema = infer_schema(raw)
    df = pd.DataFrame(index=raw.index)

    if schema.get("company"):
        df["Company"] = raw[schema["company"]].astype(str)
    else:
        df["Company"] = [f"STU-{i:05d}" for i in range(len(raw))]
    if schema.get("industry"):
        df["Industry"] = (
            raw[schema["industry"]].astype(str).str.split("|").str[0].str.strip()
        )
        df["Industry"] = df["Industry"].replace({"": "Unknown", "nan": "Unknown"}).fillna("Unknown")
    else:
        st.warning("No industry/category column detected in the dataset — industry charts will be skipped.")
        df["Industry"] = "Unknown"

    if schema.get("country"):
        df["Country"] = raw[schema["country"]].astype(str).str.strip()
    else:
        st.warning("No country column detected in the dataset — geographic charts will be skipped.")
        df["Country"] = "Unknown"

    df["Region"] = raw[schema["region"]].astype(str) if schema.get("region") else "Unknown"
    df["City"] = raw[schema["city"]].astype(str) if schema.get("city") else "Unknown"

    if schema.get("funding"):
        funding_raw = pd.to_numeric(raw[schema["funding"]], errors="coerce")
        df["Funding"] = (funding_raw / 1_000_000).round(3)
    else:
        st.warning("No funding column detected in the dataset — funding KPIs/charts will be skipped.")
        df["Funding"] = np.nan

    if schema.get("funding_rounds"):
        df["FundingRounds"] = pd.to_numeric(raw[schema["funding_rounds"]], errors="coerce")
    else:
        df["FundingRounds"] = np.nan

    
    if schema.get("status"):
        raw_status = raw[schema["status"]].astype(str).str.strip().str.lower()
        df["RawStatus"] = raw_status
        df["Status"] = np.where(raw_status.eq("closed"), "Failed", "Success")
    else:
        st.warning("No status column detected in the dataset — outcome-based KPIs/charts will be skipped.")
        df["RawStatus"] = "unknown"
        df["Status"] = "Success"

    
    if schema.get("founded_date"):
        founded = pd.to_datetime(raw[schema["founded_date"]], errors="coerce")
        current_year = datetime.now().year
        age = current_year - founded.dt.year
        
        df["CompanyAge"] = age.where((age >= 0) & (age <= 100))
    else:
        df["CompanyAge"] = np.nan

    return df


@st.cache_data
def compute_kpis(df: pd.DataFrame) -> dict:
    """Computes headline KPI metrics from the REAL dataset."""
    total_startups = len(df)
    success_rate = (df["Status"] == "Success").mean() * 100 if total_startups else 0.0
    avg_funding = df["Funding"].mean() if total_startups and df["Funding"].notna().any() else 0.0
    countries_covered = df["Country"].nunique()

    return {
        "total_startups": total_startups,
        "success_rate": success_rate,
        "avg_funding": avg_funding,
        "countries_covered": countries_covered,
    }


@st.cache_data
def get_recent_startups(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Returns a formatted sample of REAL startups from the dataset."""
    n = min(n, len(df))
    sample = df.sample(n=n, random_state=7).reset_index(drop=True) if n else df.copy()
    sample.index += 1
    sample["Funding"] = sample["Funding"].apply(lambda x: f"${x:,.1f}M" if pd.notna(x) else "—")
    return sample[["Company", "Industry", "Funding", "Country", "Status"]]

@st.cache_data
def compute_kpi_sparkline_series(df: pd.DataFrame, metric: str, points: int = 14) -> np.ndarray:
    
    fallback_value = {
        "count": len(df),
        "success_rate": (df["Status"] == "Success").mean() * 100 if len(df) else 0.0,
        "avg_funding": df["Funding"].mean() if df["Funding"].notna().any() else 0.0,
        "countries": df["Country"].nunique(),
    }.get(metric, 0.0)

    if "CompanyAge" not in df.columns or df["CompanyAge"].notna().sum() < 3:
        return np.full(points, fallback_value if pd.notna(fallback_value) else 0.0)

    current_year = datetime.now().year
    tmp = df.dropna(subset=["CompanyAge"]).copy()
    tmp["FoundedYear"] = (current_year - tmp["CompanyAge"]).astype(int)
    years = sorted(tmp["FoundedYear"].unique())
    years = years[-points:] if len(years) > points else years
    if len(years) < 3:
        return np.full(points, fallback_value if pd.notna(fallback_value) else 0.0)

    values = []
    for year in years:
        cohort = tmp[tmp["FoundedYear"] == year]
        if metric == "count":
            values.append(len(cohort))
        elif metric == "success_rate":
            values.append(cohort["Status"].eq("Success").mean() * 100 if len(cohort) else np.nan)
        elif metric == "avg_funding":
            values.append(cohort["Funding"].mean())
        elif metric == "countries":
            values.append(cohort["Country"].nunique())
        else:
            values.append(np.nan)

    series = pd.Series(values, dtype=float).interpolate(limit_direction="both").to_numpy()
    if len(series) < points:
        series = np.pad(series, (points - len(series), 0), mode="edge")
    return series


@st.cache_data
def compute_kpi_trends(df: pd.DataFrame) -> dict:
    trends = {"total_startups": None, "success_rate": None, "avg_funding": None, "countries_covered": None}
    if "CompanyAge" not in df.columns or df["CompanyAge"].notna().sum() < 10:
        return trends

    median_age = df["CompanyAge"].median()
    recent = df[df["CompanyAge"] <= median_age]   
    older = df[df["CompanyAge"] > median_age]     
    if recent.empty or older.empty:
        return trends

    def pct_delta(new_val, old_val):
        if old_val in (0, None) or pd.isna(old_val) or pd.isna(new_val):
            return None
        return (new_val - old_val) / old_val * 100

    trends["total_startups"] = pct_delta(len(recent), len(older))

    recent_sr = recent["Status"].eq("Success").mean() * 100
    older_sr = older["Status"].eq("Success").mean() * 100
    trends["success_rate"] = recent_sr - older_sr  

    trends["avg_funding"] = pct_delta(recent["Funding"].mean(), older["Funding"].mean())
    trends["countries_covered"] = pct_delta(recent["Country"].nunique(), older["Country"].nunique())
    return trends


def create_sparkline(values: np.ndarray, color: str) -> go.Figure:
    """Builds a compact, axis-free sparkline chart for KPI cards."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=values,
            mode="lines",
            line=dict(color=color, width=2.4, shape="spline"),
            fill="tozeroy",
            fillcolor=color.replace(")", ",0.14)").replace("rgb", "rgba") if "rgb" in color else color,
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=42,
        showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


@st.cache_data
def compute_leaderboard(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    ranked = df.dropna(subset=["Funding"]).sort_values("Funding", ascending=False).head(top_n).reset_index(drop=True)
    ranked.index += 1
    return ranked[["Company", "Industry", "Country", "Funding", "Status"]]


@st.cache_data
def generate_ai_insights(df: pd.DataFrame) -> list:
    
    if df.empty:
        return [("💡", "No startups match the current filters. Try widening your search.")]

    insights = []

    top_industry = df["Industry"].value_counts().idxmax()
    top_industry_share = df["Industry"].value_counts(normalize=True).max() * 100
    insights.append((
        "📊",
        f"<b>{top_industry}</b> leads the portfolio, representing "
        f"<b>{top_industry_share:.1f}%</b> of all tracked startups."
    ))

    top_country = df["Country"].value_counts().idxmax()
    insights.append((
        "🌍",
        f"<b>{top_country}</b> hosts the largest concentration of startups "
        f"in the current dataset."
    ))

    success_rate = (df["Status"] == "Success").mean() * 100
    trend_word = "healthy" if success_rate >= 55 else "cautionary"
    insights.append((
        "📈",
        f"Overall success rate stands at <b>{success_rate:.1f}%</b>, "
        f"a {trend_word} signal for this cohort."
    ))

    if df["FundingRounds"].notna().any():
        corr = df[["Funding", "FundingRounds"]].corr().iloc[0, 1]
        if pd.notna(corr):
            relation = "positively correlated" if corr > 0.05 else ("negatively correlated" if corr < -0.05 else "largely uncorrelated")
            insights.append((
                "🤖",
                f"Funding and number of funding rounds appear <b>{relation}</b> "
                f"(r = {corr:.2f}) across this sample."
            ))

    avg_funding_success = df.loc[df["Status"] == "Success", "Funding"].mean()
    avg_funding_failed = df.loc[df["Status"] == "Failed", "Funding"].mean()
    if pd.notna(avg_funding_success) and pd.notna(avg_funding_failed):
        diff = avg_funding_success - avg_funding_failed
        direction = "higher" if diff > 0 else "lower"
        insights.append((
            "💰",
            f"Successful startups raised on average <b>${abs(diff):.1f}M {direction}</b> "
            f"funding than failed ones."
        ))

    if df["CompanyAge"].notna().any():
        avg_age = df["CompanyAge"].mean()
        insights.append((
            "🕒",
            f"The average tracked startup is roughly <b>{avg_age:.1f} years</b> old, "
            f"based on founding dates in the dataset."
        ))

    return insights


def apply_aurora_layout(fig, height=380):
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter, 'Segoe UI', sans-serif", size=12.5),
        margin=dict(l=12, r=16, t=16, b=12),
        height=height,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
            font=dict(size=11.5, color=COLOR_MUTED),
        ),
        hoverlabel=dict(
            bgcolor="rgba(30,41,59,0.95)",
            font_color=COLOR_TEXT,
            font_family="Inter, sans-serif",
            font_size=12.5,
            bordercolor=COLOR_PRIMARY,
        ),
        colorway=CHART_COLORWAY,
        transition=dict(duration=350, easing="cubic-in-out"),
    )
    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.14)",
        showline=True,
        linecolor="rgba(148,163,184,0.16)",
        tickfont=dict(color=COLOR_MUTED, size=11),
    )
    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.10)",
        zerolinecolor="rgba(148,163,184,0.14)",
        showline=False,
        tickfont=dict(color=COLOR_MUTED, size=11),
    )
    return fig

def create_pie_chart(df: pd.DataFrame):
    
    if "RawStatus" not in df.columns or df.empty:
        return None

    status_counts = df["RawStatus"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    status_counts["Status"] = status_counts["Status"].str.title()
    colors = [CHART_COLORWAY[i % len(CHART_COLORWAY)] for i in range(len(status_counts))]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=status_counts["Status"],
                values=status_counts["Count"],
                hole=0.68,
                marker=dict(
                    colors=colors,
                    line=dict(color=COLOR_BG, width=4),
                ),
                textinfo="percent",
                textfont=dict(color=COLOR_TEXT, size=13, family="Inter, sans-serif"),
                pull=[0.02] * len(status_counts),
                rotation=90,
            )
        ]
    )
    fig.add_annotation(
        text="<b>Status</b><br><span style='font-size:11px;color:#94A3B8'>Split</span>",
        showarrow=False, font=dict(size=14, color=COLOR_TEXT), align="center",
    )
    return apply_aurora_layout(fig)


def create_funding_histogram(df: pd.DataFrame):
    if "Funding" not in df.columns or df["Funding"].dropna().empty:
        return None

    plot_df = df.dropna(subset=["Funding"]).copy()
    cap = plot_df["Funding"].quantile(0.99)
    plot_df = plot_df[plot_df["Funding"] <= cap]

    fig = px.histogram(
        plot_df, x="Funding", nbins=30,
        color_discrete_sequence=[COLOR_PRIMARY],
    )
    fig.update_traces(
        marker_line_color=COLOR_BG,
        marker_line_width=1.5,
        marker_color=COLOR_PRIMARY,
        opacity=0.88,
    )
    fig.update_layout(
        xaxis_title="Funding ($M)",
        yaxis_title="Number of Startups",
        bargap=0.08,
    )
    return apply_aurora_layout(fig)


def create_industry_bar_chart(df: pd.DataFrame):
    """Bar chart of top industries by REAL startup count."""
    if "Industry" not in df.columns or df.empty:
        return None

    industry_counts = df["Industry"].value_counts().nlargest(8).reset_index()
    industry_counts.columns = ["Industry", "Count"]

    fig = px.bar(
        industry_counts.sort_values("Count"),
        x="Count", y="Industry", orientation="h",
        color="Count", color_continuous_scale=[COLOR_PURPLE, COLOR_PRIMARY],
    )
    fig.update_traces(marker=dict(cornerradius=8, line=dict(width=0)))
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Startups", yaxis_title="", bargap=0.28)
    return apply_aurora_layout(fig)


def create_country_bar_chart(df: pd.DataFrame):
    """Bar chart of top countries by REAL startup count. (Kept for backend
    parity; the dashboard currently visualizes country distribution via
    the world map.)"""
    if "Country" not in df.columns or df.empty:
        return None

    country_counts = df["Country"].value_counts().nlargest(8).reset_index()
    country_counts.columns = ["Country", "Count"]

    fig = px.bar(
        country_counts.sort_values("Count"),
        x="Count", y="Country", orientation="h",
        color="Count", color_continuous_scale=[COLOR_MINT, COLOR_PRIMARY],
    )
    fig.update_traces(marker=dict(cornerradius=8, line=dict(width=0)))
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Startups", yaxis_title="", bargap=0.28)
    return apply_aurora_layout(fig)


def create_world_map(df: pd.DataFrame):
    """Interactive choropleth world map showing REAL startup distribution
    by country. clean_startups.csv already ships ISO3 country codes
    ("USA", "GBR", ...); if a different dataset provides full country
    names instead, this falls back to the COUNTRY_ISO3 lookup table."""
    if "Country" not in df.columns or df.empty:
        return None

    country_counts = df["Country"].value_counts().reset_index()
    country_counts.columns = ["Country", "Count"]

    if _is_iso3_series(country_counts["Country"]):
        country_counts["iso3"] = country_counts["Country"]
    else:
        country_counts["iso3"] = country_counts["Country"].map(COUNTRY_ISO3)

    unmapped = country_counts["iso3"].isna().sum()
    country_counts = country_counts.dropna(subset=["iso3"])
    if unmapped:
        st.warning(f"{unmapped} countries in the dataset could not be matched to a map location and were excluded from the world map.")
    if country_counts.empty:
        return None

    fig = px.choropleth(
        country_counts,
        locations="iso3",
        color="Count",
        hover_name="Country",
        color_continuous_scale=[[0, "#1E293B"], [0.5, COLOR_PURPLE], [1, COLOR_PRIMARY]],
    )
    fig.update_traces(
        marker_line_color="rgba(148,163,184,0.25)",
        marker_line_width=0.6,
    )
    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=False,
        showland=True,
        landcolor="rgba(148,163,184,0.06)",
        showocean=True,
        oceancolor="rgba(0,0,0,0)",
        showcountries=True,
        countrycolor="rgba(148,163,184,0.12)",
        projection_type="natural earth",
    )
    fig.update_layout(coloraxis_colorbar=dict(thickness=14, outlinewidth=0, tickfont=dict(color=COLOR_MUTED)))
    return apply_aurora_layout(fig, height=380)


def create_heatmap(df: pd.DataFrame):
    
    candidate_cols = [c for c in ["Funding", "FundingRounds", "CompanyAge"] if c in df.columns and df[c].notna().any()]
    if len(candidate_cols) < 2:
        return None

    numeric_df = df[candidate_cols].copy()
    numeric_df["SuccessFlag"] = (df["Status"] == "Success").astype(int)
    corr = numeric_df.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale=[[0, "#0B1120"], [0.5, COLOR_PURPLE], [1, COLOR_PRIMARY]],
            zmin=-1, zmax=1,
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
            textfont=dict(color=COLOR_TEXT, size=12.5, family="Inter, sans-serif"),
            xgap=4,
            ygap=4,
            colorbar=dict(thickness=14, outlinewidth=0, tickfont=dict(color=COLOR_MUTED, size=11), len=0.85),
        )
    )
    return apply_aurora_layout(fig, height=380)

def render_hero_section():
    now_str = datetime.now().strftime("%b %d, %Y · %I:%M %p")

    render_html(
        f"""
        <div class="hero-top-row">
            <div>
                <div class="hero-eyebrow"><span class="dot"></span>PREDICT &middot; ANALYZE &middot; EXPLORE</div>
                <div class="hero-title">Startup Success Predictor Dashboard</div>
                <div class="hero-subtitle">Data-driven Insights & Machine Learning Predictions for Smarter Startup Analysis</div>
            </div>
            <div class="hero-meta">
                
                
            </div>
        </div>
        
        """
    )


def render_kpi_ribbon(kpis: dict, df: pd.DataFrame):
    top_industry = df["Industry"].value_counts().idxmax() if len(df) else "—"
    render_html(
        f"""
        <div class="kpi-ribbon">
            <div class="ribbon-chip">📦 <b>{kpis['total_startups']:,}</b>&nbsp;startups analyzed</div>
            <div class="ribbon-chip">🏆 Top sector:&nbsp;<b>{top_industry}</b></div>
            <div class="ribbon-chip">🌐 <b>{kpis['countries_covered']}</b>&nbsp;countries covered</div>
            <div class="ribbon-chip">⚡ Data refresh:&nbsp;<b>Real-time</b></div>
        </div>
        """
    )


def create_kpi_cards(kpis: dict, df: pd.DataFrame):
    col1, col2, col3, col4 = st.columns(4)
    trends = compute_kpi_trends(df)

    def fmt_trend(metric_key):
        delta = trends.get(metric_key)
        if delta is None:
            return "flat", "→ N/A"
        direction = "up" if delta >= 0 else "down"
        arrow_val = f"{'+' if delta >= 0 else ''}{delta:.1f}%" if metric_key != "success_rate" else f"{'+' if delta >= 0 else ''}{delta:.1f}pp"
        return direction, arrow_val

    total_dir, total_val = fmt_trend("total_startups")
    success_dir, success_val = fmt_trend("success_rate")
    funding_dir, funding_val = fmt_trend("avg_funding")
    countries_dir, countries_val = fmt_trend("countries_covered")

    kpi_config = [
        (col1, "🏢", f"{kpis['total_startups']:,}", "Total Startups",
         "Tracked across all industries", total_dir, total_val, "count", COLOR_PRIMARY),
        (col2, "📈", f"{kpis['success_rate']:.1f}%", "Success Rate",
         "Based on historical outcomes", success_dir, success_val, "success_rate", COLOR_MINT),
        (col3, "💰", f"${kpis['avg_funding']:.1f}M", "Average Funding",
         "Per startup, all rounds", funding_dir, funding_val, "avg_funding", COLOR_PURPLE),
        (col4, "🌍", f"{kpis['countries_covered']}", "Countries Covered",
         "Global startup footprint", countries_dir, countries_val, "countries", "#F472B6"),
    ]

    for i, (col, icon, value, label, desc, trend_dir, trend_val, spark_metric, spark_color) in enumerate(kpi_config):
        with col:
            arrow = "▲" if trend_dir == "up" else ("▼" if trend_dir == "down" else "→")
            trend_class = "up" if trend_dir == "up" else "down"

            render_html(
                f"""
                <div class="glass-card-wrap" style="animation-delay:{i * 0.08}s;">
                    <div class="glass-card">
                        <div class="kpi-top-row">
                            <div class="kpi-icon">{icon}</div>
                            <div class="kpi-trend {trend_class}">{arrow} {trend_val}</div>
                        </div>
                        <div class="kpi-label">{label}</div>
                        <p class="kpi-value">{value}</p>
                    </div>
                """
            )
            spark_values = compute_kpi_sparkline_series(df, metric=spark_metric)
            st.plotly_chart(
                create_sparkline(spark_values, spark_color),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            render_html(
                f"""
                    <div class="kpi-card-footer">
                        <div class="kpi-desc">{desc}</div>
                    </div>
                </div>
                """
            )


def render_filter_bar(df: pd.DataFrame) -> pd.DataFrame:
    
    #st.markdown('<div class="filter-bar-wrap"><div class="filter-bar">', unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1.1, 1.1, 1.3, 1.1, 1.3])

    with c1:
        st.markdown('<div class="filter-label">Industry</div>', unsafe_allow_html=True)
        top_industries = df["Industry"].value_counts().nlargest(40).index.tolist()
        industry_options = ["All Industries"] + sorted(top_industries)
        industry_filter = st.selectbox("Industry", industry_options, label_visibility="collapsed", key="filter_industry")

    with c2:
        st.markdown('<div class="filter-label">Country</div>', unsafe_allow_html=True)
        top_countries = df["Country"].value_counts().nlargest(40).index.tolist()
        country_options = ["All Countries"] + sorted(top_countries)
        country_filter = st.selectbox("Country", country_options, label_visibility="collapsed", key="filter_country")

    with c3:
        st.markdown('<div class="filter-label">Funding Range ($M)</div>', unsafe_allow_html=True)
        funding_series = df["Funding"].dropna()
        if not funding_series.empty:
            min_funding, max_funding = float(funding_series.min()), float(funding_series.max())
        else:
            min_funding, max_funding = 0.0, 1.0
        funding_range = st.slider(
            "Funding Range", min_value=float(np.floor(min_funding)), max_value=float(np.ceil(max_funding)),
            value=(float(np.floor(min_funding)), float(np.ceil(max_funding))),
            label_visibility="collapsed", key="filter_funding",
        )

    with c4:
        st.markdown('<div class="filter-label">Status</div>', unsafe_allow_html=True)
        status_filter = st.selectbox("Status", ["All", "Success", "Failed"], label_visibility="collapsed", key="filter_status")

    with c5:
        st.markdown('<div class="filter-label">Search</div>', unsafe_allow_html=True)
        search_term = st.text_input("Search", placeholder="🔍 Search startup ID, industry, or city...", label_visibility="collapsed", key="filter_search")

    #st.markdown('</div></div>', unsafe_allow_html=True)

    filtered = df.copy()
    if industry_filter != "All Industries":
        filtered = filtered[filtered["Industry"] == industry_filter]
    if country_filter != "All Countries":
        filtered = filtered[filtered["Country"] == country_filter]
    if status_filter != "All":
        filtered = filtered[filtered["Status"] == status_filter]
    filtered = filtered[filtered["Funding"].between(funding_range[0], funding_range[1]) | filtered["Funding"].isna()]
    if search_term:
        haystack = (
            filtered["Company"].astype(str) + " " +
            filtered["Industry"].astype(str) + " " +
            filtered["City"].astype(str)
        )
        filtered = filtered[haystack.str.contains(search_term, case=False, na=False)]

    return filtered


def render_chart_card(title: str, subtitle: str, fig):
    render_html(
        f"""<div class="chart-card-wrap">
            <div class="chart-card">
                <div class="chart-title">{title}</div>
                <div class="chart-sub">{subtitle}</div>
        """
    )
    if fig is None:
        st.info("This chart isn't available — the dataset is missing the column(s) it needs.")
    else:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_charts_section(df: pd.DataFrame):
    
    st.markdown(
        '<div class="section-header">Performance Overview'
        '<span class="section-sub">Visual breakdown of the current dataset</span></div>',
        unsafe_allow_html=True,
    )

    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        render_chart_card("Startup Status", "Operating / acquired / IPO / closed breakdown", create_pie_chart(df))
    with row1_col2:
        render_chart_card("Funding Distribution", "Spread of total funding raised across startups", create_funding_histogram(df))

    
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        render_chart_card("Top Industries", "Most represented sectors by startup count", create_industry_bar_chart(df))
    with row2_col2:
        render_chart_card("Global Startup Distribution", "Interactive map of startup density by country", create_world_map(df))

    
    render_chart_card("Correlation Heatmap", "Relationship between funding, funding rounds, company age, and success", create_heatmap(df))


def render_ai_insights_panel(df: pd.DataFrame):
    """Renders an AI Insights panel summarizing the current dataset."""
    st.markdown(
        '<div class="section-header">AI Insights'
        '<span class="section-sub">Auto-generated summary of current data</span></div>',
        unsafe_allow_html=True,
    )
    insights = generate_ai_insights(df)

    st.markdown('<div class="chart-card-wrap"><div class="chart-card">', unsafe_allow_html=True)
    for icon, text in insights:
        render_html(
            f"""<div class="insight-card">
                    <div class="insight-icon">{icon}</div>
                    <div class="insight-text">{text}</div>
                </div>"""
        )
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_leaderboard(df: pd.DataFrame):
    """Renders the Top Performing Startups leaderboard card."""
    st.markdown(
        '<div class="section-header">Top Performing Startups'
        '<span class="section-sub">Ranked by total funding raised</span></div>',
        unsafe_allow_html=True,
    )
    leaderboard_df = compute_leaderboard(df, top_n=5)

    st.markdown('<div class="chart-card-wrap"><div class="chart-card">', unsafe_allow_html=True)
    medal_classes = {1: "gold", 2: "silver", 3: "bronze"}
    medal_icons = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, row in leaderboard_df.iterrows():
        rank_class = medal_classes.get(rank, "")
        rank_display = medal_icons.get(rank, f"#{rank}")
        badge_class = "badge-success" if row["Status"] == "Success" else "badge-failed"
        render_html(
            f"""
            <div class="leader-row">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div class="leader-rank {rank_class}">{rank_display}</div>
                    <div>
                        <div class="leader-name">{row['Company']}</div>
                        <div class="leader-sub">{row['Industry']} · {row['Country']}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:14px;">
                    <span class="{badge_class}">{row['Status']}</span>
                    <span class="leader-funding">${row['Funding']:,.1f}M</span>
                </div>
            </div>
            """
        )
    st.markdown('</div></div>', unsafe_allow_html=True)


def render_recent_startups_table(df: pd.DataFrame):
    """Renders the recent startups table with premium styling and status badges."""
    st.markdown(
        '<div class="section-header">Recent Startups'
        '<span class="section-sub">Latest entries in the tracked dataset</span></div>',
        unsafe_allow_html=True,
    )
    recent_df = get_recent_startups(df, n=10)

    rows_html = ""
    for _, row in recent_df.iterrows():
        badge_class = "badge-success" if row["Status"] == "Success" else "badge-failed"
        rows_html += f"""
            <tr>
                <td><b>{row['Company']}</b></td>
                <td>{row['Industry']}</td>
                <td>{row['Funding']}</td>
                <td>{row['Country']}</td>
                <td><span class="{badge_class}">{row['Status']}</span></td>
            </tr>
        """

    render_html(
        f"""
        <div class="aurora-table-wrap">
            <div class="aurora-table">
                <table class="aurora-html-table">
                    <thead>
                        <tr>
                            <th>Startup ID</th>
                            <th>Industry</th>
                            <th>Funding</th>
                            <th>Country</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html if rows_html else '<tr><td colspan="5" style="text-align:center; padding:20px;">No startups match the current filters.</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
        """
    )


def render_sidebar():
    """Renders the sidebar navigation, branding, active state, version badge, and footer."""
    with st.sidebar:
        render_html(
            f"""
            <div style="display:flex; align-items:center; gap:12px; padding:0.6rem 0 1rem 0;">
               </div>
                <div>
                    <div style="font-family:'Manrope','Inter',sans-serif; font-weight:700; font-size:1.5rem; color:{COLOR_TEXT}; letter-spacing:-0.01em;">Startup Success Predictor</div>
                    <div style="font-size:0.72rem; color:{COLOR_MUTED}; letter-spacing:0.02em;">Startup Analytics Platform</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:1.4rem;">
                <span class="version-badge">✓ Machine Learning Model </span>
            </div>
            """
        )

        render_html(
            f"<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.1em; "
            f"text-transform:uppercase; color:{COLOR_MUTED}; margin-bottom:0.6rem;'>Navigation</div>"
        )

        nav_items = [
            ("🏠","Home"),
            ("📊", "Dashboard"),
            ("📈", "Analytics"),
            ("🔍", "Explorer"),
            ("🤖", "Prediction"),
            ("ℹ️", "About"),
        ]

        if "active_nav" not in st.session_state:
            st.session_state.active_nav = "Dashboard"

        for icon, label in nav_items:
            is_active = st.session_state.active_nav == label
            if is_active:
                render_html(f'<div class="nav-active">{icon} &nbsp;{label}</div>')
            else:
                if st.button(f"{icon}   {label}", key=f"nav_{label}", use_container_width=True):
                    st.session_state.active_nav = label
                    st.rerun()

        

def main():
    """Main entry point that assembles the full Dashboard page."""
    inject_custom_css()
    render_sidebar()
    render_loading_skeleton()

    try:
        df = load_startup_data()
    except FileNotFoundError:
        st.error(
            f"Couldn't find **{DATA_FILENAME}**. Place it in the same folder "
            "as Dashboard.py (or the app's working directory) and reload."
        )
        st.stop()
    except Exception as exc:  # noqa: BLE001 - surface any other load error clearly
        st.error(f"Failed to load {DATA_FILENAME}: {exc}")
        st.stop()

    if df.empty:
        st.warning("The dataset loaded successfully but contains no rows.")
        st.stop()

    # Hero section
    render_hero_section()

    base_kpis = compute_kpis(df)
    render_kpi_ribbon(base_kpis, df)

    
    filtered_df = render_filter_bar(df)
    if filtered_df.empty:
        st.info("No startups match your filters — showing the full dataset instead.")
        filtered_df = df

    
    kpis = compute_kpis(filtered_df)
    create_kpi_cards(kpis, filtered_df)


    render_charts_section(filtered_df)

    
    insights_col, leaderboard_col = st.columns([1.15, 1])
    with insights_col:
        render_ai_insights_panel(filtered_df)
    with leaderboard_col:
        render_leaderboard(filtered_df)

    
    render_recent_startups_table(filtered_df)

  
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
