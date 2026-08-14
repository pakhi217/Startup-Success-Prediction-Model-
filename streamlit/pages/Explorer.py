import streamlit as st
import pandas as pd
from pathlib import Path

# Page setup

st.set_page_config(
    page_title="Startup Explorer",
    page_icon="🔍",
    layout="wide"
)

# Styling

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(56, 189, 248, 0.14), transparent 35%),
            radial-gradient(circle at 90% 10%, rgba(168, 85, 247, 0.12), transparent 40%),
            #0B1120;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .explorer-title {
        font-size: 2.7rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        color: #38BDF8;
    }

    .explorer-subtitle {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    .stat-card {
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.85),
            rgba(15, 23, 42, 0.85)
        );
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    }

    .stat-label {
        color: #94A3B8;
        font-size: 0.8rem;
        margin-bottom: 0.25rem;
    }

    .stat-value {
        color: #F8FAFC;
        font-size: 1.65rem;
        font-weight: 750;
    }

    .section-title {
        color: #F8FAFC;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        padding-left: 0.8rem;
        border-left: 4px solid #38BDF8;
    }

    .section-description {
        color: #94A3B8;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    div[data-baseweb="select"] > div {
        background-color: #DFF3FF !important;
        border: 1px solid #7DD3FC !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] span {
        color: #0F172A !important;
    }

    div[data-baseweb="select"] svg {
        fill: #0369A1 !important;
    }

    div[role="listbox"] {
        background-color: #E8F7FF !important;
    }

    div[role="option"] {
        color: #0F172A !important;
    }

    div[role="option"]:hover {
        background-color: #BAE6FD !important;
    }

    div[role="option"][aria-selected="true"] {
        background-color: #BAE6FD !important;
        color: #0F172A !important;
    }

    div[data-testid="stSelectbox"] label {
        color: #FFFFFF !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #DFF3FF !important;
    }

    div[data-testid="stDataFrame"] {
        background-color: #DFF3FF !important;
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #7DD3FC;
    }

    .explorer-info {
        background: linear-gradient(
            135deg,
            rgba(56, 189, 248, 0.08),
            rgba(168, 85, 247, 0.08)
        );
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        color: #CBD5E1;
        margin-bottom: 1.2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Load data

@st.cache_data
def load_startup_data():

    data_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "cleaned"
        / "clean_startups.csv"
    )

    return pd.read_csv(data_path)


df = load_startup_data()

# Header

st.markdown(
    '<div class="explorer-title">🔍 Startup Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="explorer-subtitle">'
    'Search, filter, and explore startup data.'
    '</div>',
    unsafe_allow_html=True
)

# Statistics

total_startups = len(df)
total_industries = df["industry"].nunique()
total_countries = df["country"].nunique()

stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Total Startups</div>
            <div class="stat-value">{total_startups:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Industries</div>
            <div class="stat-value">{total_industries:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with stat3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Countries</div>
            <div class="stat-value">{total_countries:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Filters

st.markdown(
    '<div class="section-title">Explore Startups</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Use the filters below to narrow down the startups you want to explore.'
    '</div>',
    unsafe_allow_html=True
)

filtered_df = df.copy()

col1, col2, col3 = st.columns(3)

with col1:
    industry_options = ["All"] + sorted(
        df["industry"].dropna().astype(str).unique().tolist()
    )

    selected_industry = st.selectbox(
        "Industry",
        industry_options
    )

with col2:
    country_options = ["All"] + sorted(
        df["country"].dropna().astype(str).unique().tolist()
    )

    selected_country = st.selectbox(
        "Country",
        country_options
    )

with col3:
    status_options = ["All"] + sorted(
        df["status"].dropna().astype(str).unique().tolist()
    )

    selected_status = st.selectbox(
        "Status",
        status_options
    )

# Apply filters

if selected_industry != "All":
    filtered_df = filtered_df[
        filtered_df["industry"] == selected_industry
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ]

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]

# Results

st.markdown(
    f"""
    <div class="explorer-info">
        Showing <strong>{len(filtered_df):,}</strong>
        startups matching your selected filters.
    </div>
    """,
    unsafe_allow_html=True
)

# Startup data

st.markdown(
    '<div class="section-title">Startup Data</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=500
)

# Startup details

st.markdown(
    '<div class="section-title">Startup Details</div>',
    unsafe_allow_html=True
)

if len(filtered_df) > 0:

    selected_index = st.selectbox(
        "Select a startup record",
        filtered_df.index.tolist(),
        format_func=lambda x: f"Startup record #{x + 1}"
    )

    startup = filtered_df.loc[selected_index]

    detail1, detail2, detail3 = st.columns(3)

    with detail1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Industry</div>
                <div class="stat-value">{startup["industry"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Country</div>
                <div class="stat-value">{startup["country"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Status</div>
                <div class="stat-value">{startup["status"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Region</div>
                <div class="stat-value">{startup["region"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with detail3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">City</div>
                <div class="stat-value">{startup["city"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Funding Rounds</div>
                <div class="stat-value">{startup["funding_rounds"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning("No startups found for the selected filters.")