import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Prediction", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

COLOR_BG = "#0B1120"
COLOR_PRIMARY = "#38BDF8"
COLOR_PURPLE = "#A855F7"
COLOR_MINT = "#2DD4BF"
COLOR_TEXT = "#F8FAFC"
COLOR_MUTED = "#94A3B8"
COLOR_DANGER = "#F87171"
COLOR_WARNING = "#FACC15"


def render_html(html: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in html.strip("\n").splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def render_box(inner_html: str) -> None:
    """Renders one fully self-contained bordered box in a SINGLE st.markdown
    call. Never split a box's opening tag, content, and closing tag across
    multiple calls - Streamlit renders each call as an isolated HTML
    fragment, so a dangling open tag renders as an empty styled shell and
    everything after it loses the wrapper entirely."""
    render_html(f'<div class="chart-card-wrap"><div class="chart-card">{inner_html}</div></div>')


def inject_custom_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', sans-serif; }}
        .stApp {{
            background:
                radial-gradient(circle at 12% 8%, rgba(56,189,248,0.14), transparent 42%),
                radial-gradient(circle at 88% 5%, rgba(168,85,247,0.16), transparent 48%),
                radial-gradient(circle at 60% 90%, rgba(45,212,191,0.10), transparent 50%),
                {COLOR_BG};
            background-size: 200% 200%;
            animation: auroraDrift 24s ease-in-out infinite;
            color: {COLOR_TEXT};
        }}
        @keyframes auroraDrift {{ 0% {{background-position:0% 0%;}} 50% {{background-position:100% 60%;}} 100% {{background-position:0% 0%;}} }}
        @keyframes fadeSlideUp {{ from {{opacity:0; transform:translateY(14px);}} to {{opacity:1; transform:translateY(0);}} }}
        .block-container {{ padding-top: 1.6rem !important; padding-bottom: 2rem !important; max-width: 1440px; }}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
        div[data-testid="stToolbar"] {{visibility: hidden; height: 0;}}
        div[data-testid="stDecoration"] {{display: none;}}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(15,23,42,0.98) 0%, rgba(11,17,32,0.99) 100%);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(148,163,184,0.10);
        }}
        section[data-testid="stSidebar"] .stButton button {{
            width: 100%; text-align: left; background: rgba(255,255,255,0.02); color: {COLOR_TEXT};
            border: 1px solid rgba(148,163,184,0.08); border-radius: 12px; padding: 0.6rem 1rem;
            margin-bottom: 6px; font-weight: 500; transition: all 0.28s ease;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            border: 1px solid rgba(56,189,248,0.45); color: {COLOR_PRIMARY}; transform: translateX(5px);
        }}
        .nav-active {{
            background: linear-gradient(90deg, rgba(56,189,248,0.16), rgba(168,85,247,0.10)) !important;
            border: 1px solid rgba(56,189,248,0.4) !important; border-left: 3px solid {COLOR_PRIMARY} !important;
            border-radius: 10px; padding: 0.6rem 1rem 0.6rem 0.85rem; margin-bottom: 6px;
            font-weight: 700; color: {COLOR_PRIMARY} !important; font-size: 0.92rem; display: flex; align-items: center; gap: 10px;
        }}

        .hero-eyebrow {{
            display: inline-flex; align-items: center; gap: 8px; font-family: 'Space Grotesk', sans-serif;
            font-size: 0.75rem; font-weight: 600; letter-spacing: 0.10em; text-transform: uppercase; color: {COLOR_PRIMARY};
            background: rgba(56,189,248,0.10); border: 1px solid rgba(56,189,248,0.25);
            padding: 5px 14px; border-radius: 999px; margin-bottom: 1rem; animation: fadeSlideUp 0.6s ease;
        }}
        .hero-title {{
            font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; line-height: 1.12; font-weight: 700;
            background: linear-gradient(100deg, {COLOR_TEXT} 10%, {COLOR_PRIMARY} 45%, {COLOR_PURPLE} 70%, {COLOR_MINT} 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            margin-bottom: 0.35rem; animation: fadeSlideUp 0.7s ease;
        }}
        .hero-subtitle {{ font-size: 1.02rem; color: {COLOR_MUTED}; margin-bottom: 1.2rem; animation: fadeSlideUp 0.8s ease; }}

        .section-header {{
            font-family: 'Space Grotesk', sans-serif; font-size: 1.28rem; font-weight: 700; color: {COLOR_TEXT};
            margin-top: 2.2rem; margin-bottom: 1rem; padding-left: 0.85rem; position: relative;
            display: flex; align-items: center; animation: fadeSlideUp 0.6s ease both;
        }}
        .section-header::before {{
            content: ""; position: absolute; left: 0; top: 50%; transform: translateY(-50%);
            width: 4px; height: 1.4rem; border-radius: 10px; background: linear-gradient(180deg, {COLOR_PRIMARY}, {COLOR_PURPLE});
        }}
        .section-sub {{ font-size: 0.85rem; color: {COLOR_MUTED}; margin-left: 0.6rem; }}

        .chart-card-wrap {{
            position: relative; border-radius: 21px; padding: 1.5px; margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(148,163,184,0.14), rgba(168,85,247,0.22) 55%, rgba(56,189,248,0.20) 100%);
            animation: fadeSlideUp 0.65s ease both;
        }}
        .chart-card {{
            background: linear-gradient(160deg, rgba(30,41,59,0.72), rgba(15,23,42,0.72));
            backdrop-filter: blur(18px); border-radius: 19.5px; padding: 1.3rem 1.4rem 0.9rem 1.4rem; box-shadow: 0 10px 32px rgba(0,0,0,0.32);
        }}
        .chart-title {{
            font-family: 'Space Grotesk', sans-serif; font-size: 1.04rem; font-weight: 700; color: {COLOR_TEXT};
            margin-bottom: 0.15rem; display: flex; align-items: center; gap: 8px;
        }}
        .chart-title::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_MINT}); }}
        .chart-sub {{ font-size: 0.78rem; color: {COLOR_MUTED}; margin-bottom: 0.7rem; }}

        .wizard-track {{ display: flex; align-items: center; justify-content: center; gap: 8px; margin: 1.5rem 0 2rem 0; }}
        .wizard-dot {{
            width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.85rem; background: rgba(148,163,184,0.10); color: {COLOR_MUTED};
            border: 2px solid rgba(148,163,184,0.18); transition: all 0.3s ease;
        }}
        .wizard-dot.active {{
            background: linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_PURPLE}); color: white; border-color: transparent;
            box-shadow: 0 0 16px rgba(56,189,248,0.5);
        }}
        .wizard-dot.done {{ background: rgba(45,212,191,0.16); color: {COLOR_MINT}; border-color: rgba(45,212,191,0.4); }}
        .wizard-line {{ width: 50px; height: 2px; background: rgba(148,163,184,0.18); }}
        .wizard-line.done {{ background: linear-gradient(90deg, {COLOR_MINT}, {COLOR_PRIMARY}); }}
        .wizard-label {{ text-align: center; font-size: 0.8rem; color: {COLOR_MUTED}; margin-bottom: 0.4rem; }}

        .risk-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 8px 20px; border-radius: 999px; font-weight: 700; font-size: 0.95rem; margin-right: 8px; }}
        .risk-low {{ background: rgba(45,212,191,0.14); color: {COLOR_MINT}; border: 1px solid rgba(45,212,191,0.4); }}
        .risk-medium {{ background: rgba(250,204,21,0.14); color: {COLOR_WARNING}; border: 1px solid rgba(250,204,21,0.4); }}
        .risk-high {{ background: rgba(248,113,113,0.14); color: {COLOR_DANGER}; border: 1px solid rgba(248,113,113,0.4); }}
        .outcome-pill {{
            display: inline-flex; align-items: center; gap: 6px; background: rgba(168,85,247,0.12);
            border: 1px solid rgba(168,85,247,0.35); color: #c4b5fd; padding: 8px 18px;
            border-radius: 999px; font-size: 0.95rem; font-weight: 700;
        }}
        .tip-card {{
            background: linear-gradient(135deg, rgba(56,189,248,0.07), rgba(168,85,247,0.07));
            border: 1px solid rgba(148,163,184,0.14); border-radius: 16px; padding: 0.95rem 1.1rem;
            margin-bottom: 0.7rem; display: flex; gap: 12px; align-items: flex-start;
        }}
        .tip-icon {{ font-size: 1.15rem; margin-top: 1px; }}
        .tip-text {{ font-size: 0.86rem; color: {COLOR_TEXT}; line-height: 1.45; }}
        .warn-note {{ font-size: 0.78rem; color: {COLOR_WARNING}; margin-top: 0.6rem; }}

        div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {{
            background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; border: 1px solid rgba(148,163,184,0.18) !important;
        }}
        .stTextInput > div > div > input, .stNumberInput > div > div > input {{
            background: rgba(255,255,255,0.03); border-radius: 10px; border: 1px solid rgba(148,163,184,0.18); color: {COLOR_TEXT};
        }}
        div[data-testid="stSlider"] > div > div > div > div {{ background: linear-gradient(90deg, {COLOR_PRIMARY}, {COLOR_PURPLE}); }}
        .stButton > button {{
            border-radius: 12px; border: 1px solid rgba(56,189,248,0.4);
            background: linear-gradient(90deg, rgba(56,189,248,0.15), rgba(168,85,247,0.15));
            color: {COLOR_TEXT}; font-weight: 600; padding: 0.55rem 1.15rem; transition: all 0.3s ease;
        }}
        .stButton > button:hover {{ border: 1px solid {COLOR_PRIMARY}; box-shadow: 0 0 20px rgba(56,189,248,0.4); transform: translateY(-2px); }}
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-track {{ background: {COLOR_BG}; }}
        ::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, {COLOR_PRIMARY}, {COLOR_PURPLE}); border-radius: 10px; }}

        /* Restyle native st.container(border=True) to match the card look.
           Using native containers (instead of raw HTML divs) for anything
           that mixes text + charts guarantees correct nesting - a hand
           written <div> split across multiple st.markdown/st.plotly_chart
           calls renders as an empty shell in Streamlit. */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border: none !important;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{
            background: linear-gradient(160deg, rgba(30,41,59,0.72), rgba(15,23,42,0.72));
            border: 1px solid rgba(148,163,184,0.14);
            border-radius: 19.5px;
            padding: 1.3rem 1.4rem 0.9rem 1.4rem;
            box-shadow: 0 10px 32px rgba(0,0,0,0.32);
            margin-bottom: 1.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        render_html(
            f"""
            <div style="padding:0.6rem 0 1rem 0;">
                <div style="font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.4rem; color:{COLOR_TEXT};">🚀 Startup Success Predictor</div>
                <div style="font-size:0.72rem; color:{COLOR_MUTED};">Startup Analytics Platform</div>
            </div>
            """
        )
        nav_items = [("🏠", "Home"), ("📊", "Dashboard"), ("📈", "Analytics"), ("🤖", "Prediction"), ("ℹ️", "About")]
        page_map = {
            "Home": "Home.py",
            "Dashboard": "Dashboard.py",
            "Analytics": "Analytics.py",
            "Prediction": "Prediction.py",
            "About": "About.py",
        }
        for icon, label in nav_items:
            if label == "Prediction":
                render_html(f'<div class="nav-active">{icon} &nbsp;{label}</div>')
            else:
                if st.button(f"{icon}   {label}", key=f"nav_{label}", use_container_width=True):
                    st.switch_page(f"pages/{page_map[label]}")
        st.markdown("---")
        st.caption("Version 1.0")


def _resolve_path(filename: str, subfolder: str = "models") -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here / filename,
        here.parent / subfolder / filename,
        here.parent.parent / subfolder / filename,
        Path.cwd() / subfolder / filename,
        Path(filename),
    ]
    for c in candidates:
        if c.exists():
            return c
    return Path(filename)


@st.cache_resource
def load_artifacts():
    model = None
    encoders = None
    scaler = None

    try:
        model = joblib.load(_resolve_path("best_model.pkl"))
    except Exception as e:
        st.error(f"Couldn't load best_model.pkl: {e}")

    try:
        encoders = joblib.load(_resolve_path("encoder.pkl"))
    except Exception as e:
        st.error(f"Couldn't load encoder.pkl: {e}")

    try:
        scaler = joblib.load(_resolve_path("scaler.pkl"))
    except Exception as e:
        st.error(f"Couldn't load scaler.pkl: {e}")

    return model, encoders, scaler


@st.cache_data
def get_sorted_classes(_encoders, col: str, limit: int = 5000):
    """Returns a sorted list of known values for a dropdown. Capped to avoid
    freezing the browser on columns with extreme cardinality (industry/city
    can have tens of thousands of unique values)."""
    classes = sorted(list(_encoders[col].classes_))
    if len(classes) > limit:
        return classes[:limit]
    return classes


if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


def render_progress_tracker(current_step: int, total: int = 3):
    labels = ["Company Basics", "Funding Metrics", "Review & Predict"]
    dots_html = '<div class="wizard-track">'
    for i in range(1, total + 1):
        state = "active" if i == current_step else ("done" if i < current_step else "")
        dots_html += f'<div class="wizard-dot {state}">{"✓" if i < current_step else i}</div>'
        if i < total:
            line_state = "done" if i < current_step else ""
            dots_html += f'<div class="wizard-line {line_state}"></div>'
    dots_html += "</div>"
    render_html(dots_html)
    render_html(f'<div class="wizard-label">Step {current_step} of {total} — <b>{labels[current_step-1]}</b></div>')


def safe_encode(encoders: dict, col: str, raw_value: str):
    le = encoders[col]
    classes = list(le.classes_)
    if raw_value in classes:
        matched = raw_value
    else:
        lower_map = {c.lower(): c for c in classes}
        if raw_value.lower() in lower_map:
            matched = lower_map[raw_value.lower()]
        else:
            contains = [c for c in classes if raw_value.lower() in c.lower()]
            matched = contains[0] if contains else classes[0]
    code = le.transform([matched])[0]
    was_exact = matched.lower() == raw_value.lower()
    return code, matched, was_exact


def build_feature_vector(form_data: dict, encoders: dict, scaler):
    match_notes = {}

    industry_code, industry_matched, industry_exact = safe_encode(encoders, "industry", form_data["category"])
    country_code, country_matched, country_exact = safe_encode(encoders, "country", form_data["country"])
    region_code, region_matched, region_exact = safe_encode(encoders, "region", form_data["region"])
    city_code, city_matched, city_exact = safe_encode(encoders, "city", form_data["city"])

    match_notes["industry"] = (industry_matched, industry_exact)
    match_notes["country"] = (country_matched, country_exact)
    match_notes["region"] = (region_matched, region_exact)
    match_notes["city"] = (city_matched, city_exact)

    current_year = datetime.now().year
    company_age = max(current_year - form_data["founded_year"], 0)
    total_funding_dollars = form_data["funding_total"] * 1_000_000

    numeric_df = pd.DataFrame(
        [
            {
                "total_funding": total_funding_dollars,
                "funding_rounds": form_data["funding_rounds"],
                "company_age": company_age,
            }
        ]
    )
    scaled = scaler.transform(numeric_df[["total_funding", "funding_rounds", "company_age"]])[0]

    feature_vector = np.array(
        [
            industry_code,
            scaled[0],
            country_code,
            region_code,
            city_code,
            scaled[1],
            scaled[2],
        ]
    ).reshape(1, -1)

    return feature_vector, match_notes


def get_prediction(model, encoders, feature_vector):
    pred_code = model.predict(feature_vector)[0]
    probs = model.predict_proba(feature_vector)[0]
    status_classes = encoders["status"].classes_
    pred_label = encoders["status"].inverse_transform([pred_code])[0]

    prob_by_label = {status_classes[i]: probs[i] for i in range(len(status_classes))}
    closed_key = next((c for c in status_classes if c.lower() == "closed"), None)
    survival_prob = 1 - prob_by_label[closed_key] if closed_key else max(probs)

    return pred_label, prob_by_label, survival_prob


def render_gauge(probability: float):
    pct = probability * 100
    color = COLOR_MINT if pct >= 65 else (COLOR_WARNING if pct >= 40 else COLOR_DANGER)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct,
            number={"suffix": "%", "font": {"size": 42, "color": COLOR_TEXT, "family": "Space Grotesk"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": COLOR_MUTED, "tickfont": {"color": COLOR_MUTED}},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(248,113,113,0.14)"},
                    {"range": [40, 65], "color": "rgba(250,204,21,0.14)"},
                    {"range": [65, 100], "color": "rgba(45,212,191,0.14)"},
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": COLOR_TEXT, "family": "Inter"},
        height=260,
        margin=dict(l=20, r=20, t=30, b=10),
    )
    return fig


def risk_badge_html(probability: float) -> str:
    pct = probability * 100
    if pct >= 65:
        return '<span class="risk-badge risk-low">🟢 Low Risk</span>'
    elif pct >= 40:
        return '<span class="risk-badge risk-medium">🟡 Medium Risk</span>'
    else:
        return '<span class="risk-badge risk-high">🔴 High Risk</span>'


def render_class_probability_chart(prob_by_label: dict):
    df = pd.DataFrame(
        {
            "Outcome": [k.title() for k in prob_by_label.keys()],
            "Probability": [v * 100 for v in prob_by_label.values()],
        }
    )
    df = df.sort_values("Probability", ascending=True)
    fig = px.bar(
        df, x="Probability", y="Outcome", orientation="h", color="Probability",
        color_continuous_scale=[COLOR_PURPLE, COLOR_PRIMARY],
    )
    fig.update_traces(marker=dict(cornerradius=8, line=dict(width=0)), texttemplate="%{x:.1f}%", textposition="outside")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter"),
        coloraxis_showscale=False,
        margin=dict(l=12, r=40, t=16, b=12),
        height=280,
        xaxis=dict(range=[0, 100], gridcolor="rgba(148,163,184,0.10)", tickfont=dict(color=COLOR_MUTED)),
        yaxis=dict(tickfont=dict(color=COLOR_MUTED)),
    )
    return fig


def render_feature_importance(model):
    if not hasattr(model, "feature_importances_"):
        return None
    feature_names = ["Industry", "Total Funding", "Country", "Region", "City", "Funding Rounds", "Company Age"]
    importances = model.feature_importances_
    n = min(len(importances), len(feature_names))
    imp_df = pd.DataFrame({"Feature": feature_names[:n], "Importance": importances[:n]}).sort_values(
        "Importance", ascending=True
    )
    fig = px.bar(
        imp_df, x="Importance", y="Feature", orientation="h", color="Importance",
        color_continuous_scale=[COLOR_PURPLE, COLOR_PRIMARY],
    )
    fig.update_traces(marker=dict(cornerradius=8, line=dict(width=0)))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLOR_TEXT, family="Inter"),
        coloraxis_showscale=False,
        margin=dict(l=12, r=16, t=16, b=12),
        height=320,
        xaxis=dict(gridcolor="rgba(148,163,184,0.10)", tickfont=dict(color=COLOR_MUTED)),
        yaxis=dict(tickfont=dict(color=COLOR_MUTED)),
    )
    return fig


def generate_tips(form_data: dict, pred_label: str, survival_prob: float) -> list:
    tips = []
    if form_data["funding_rounds"] < 2:
        tips.append(
            (
                "💰",
                "Startups with more funding rounds tend to show stronger survival signals in this dataset — consider planning your next raise.",
            )
        )
    if pred_label.lower() == "closed":
        tips.append(
            (
                "⚠️",
                "The model's top predicted outcome for these inputs is 'Closed'. Revisit funding strategy and market positioning before your next milestone.",
            )
        )
    elif pred_label.lower() == "operating":
        tips.append(("✅", "Your inputs align most closely with startups that remained operating in this dataset."))
    else:
        tips.append(("✅", f"Your inputs align most closely with startups that reached '{pred_label.title()}' in this dataset."))
    tips.append(
        (
            "📊",
            "This prediction reflects historical patterns from a training dataset only — it isn't financial advice, and real outcomes depend on many factors outside this data.",
        )
    )
    return tips


def _select_index(options, current_value):
    if current_value in options:
        return options.index(current_value)
    return 0


def render_step_1(encoders):
    fd = st.session_state.form_data

    industry_options = get_sorted_classes(encoders, "industry")
    country_options = get_sorted_classes(encoders, "country")
    region_options = get_sorted_classes(encoders, "region")
    city_options = get_sorted_classes(encoders, "city")

    with st.container(border=True):
        render_html(
            '<div class="chart-title">Company Basics</div>'
            '<div class="chart-sub">Choose the closest match — these lists come directly from the training data</div>'
        )
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox(
                "Industry / Category", industry_options,
                index=_select_index(industry_options, fd.get("category", "Software")),
                key="in_category",
            )
            country = st.selectbox(
                "Country (ISO3 code)", country_options,
                index=_select_index(country_options, fd.get("country", "USA")),
                key="in_country",
            )
        with c2:
            region = st.selectbox(
                "Region / State", region_options,
                index=_select_index(region_options, fd.get("region", region_options[0] if region_options else "")),
                key="in_region",
            )
            city = st.selectbox(
                "City", city_options,
                index=_select_index(city_options, fd.get("city", city_options[0] if city_options else "")),
                key="in_city",
            )
        founded_year = st.slider(
            "Founding Year", min_value=1990, max_value=datetime.now().year,
            value=fd.get("founded_year", 2020), key="in_founded_year",
        )

    col_next = st.columns([3, 1])[1]
    with col_next:
        if st.button("Next →", use_container_width=True, key="step1_next"):
            st.session_state.form_data.update(
                {
                    "category": category,
                    "country": country,
                    "region": region,
                    "city": city,
                    "founded_year": founded_year,
                }
            )
            st.session_state.wizard_step = 2
            st.rerun()


def render_step_2():
    fd = st.session_state.form_data
    with st.container(border=True):
        render_html('<div class="chart-title">Funding Metrics</div><div class="chart-sub">Financial signals used by the model</div>')
        c1, c2 = st.columns(2)
        with c1:
            funding_total = st.number_input(
                "Total Funding Raised ($M)", min_value=0.0, value=fd.get("funding_total", 1.0), step=0.1, key="in_funding_total"
            )
        with c2:
            funding_rounds = st.number_input(
                "Number of Funding Rounds", min_value=0, value=fd.get("funding_rounds", 1), step=1, key="in_funding_rounds"
            )

    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("← Back", use_container_width=True, key="step2_back"):
            st.session_state.wizard_step = 1
            st.rerun()
    with cb2:
        if st.button("Next →", use_container_width=True, key="step2_next"):
            st.session_state.form_data.update(
                {"funding_total": funding_total, "funding_rounds": funding_rounds}
            )
            st.session_state.wizard_step = 3
            st.rerun()


def render_step_3(model, encoders, scaler):
    fd = st.session_state.form_data
    with st.container(border=True):
        render_html('<div class="chart-title">Review Your Inputs</div><div class="chart-sub">Confirm before running the prediction</div>')
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.markdown(f"**Category:** {fd.get('category')}")
            st.markdown(f"**Country:** {fd.get('country')}")
        with rc2:
            st.markdown(f"**Region:** {fd.get('region')}")
            st.markdown(f"**City:** {fd.get('city')}")
        with rc3:
            st.markdown(f"**Founded:** {fd.get('founded_year')}")
            st.markdown(f"**Funding:** ${fd.get('funding_total')}M across {fd.get('funding_rounds')} round(s)")

    cb1, cb2 = st.columns(2)
    with cb1:
        if st.button("← Back", use_container_width=True, key="step3_back"):
            st.session_state.wizard_step = 2
            st.rerun()
    with cb2:
        if st.button("🔮 Predict Outcome", use_container_width=True, key="step3_predict"):
            feature_vector, match_notes = build_feature_vector(fd, encoders, scaler)
            pred_label, prob_by_label, survival_prob = get_prediction(model, encoders, feature_vector)
            st.session_state.prediction_result = {
                "pred_label": pred_label,
                "prob_by_label": prob_by_label,
                "survival_prob": survival_prob,
                "match_notes": match_notes,
            }
            st.session_state.wizard_step = 4
            st.rerun()


def render_step_4(model, encoders, scaler):
    fd = st.session_state.form_data
    result = st.session_state.prediction_result
    pred_label = result["pred_label"]
    prob_by_label = result["prob_by_label"]
    survival_prob = result["survival_prob"]
    match_notes = result["match_notes"]

    st.markdown(
        '<div class="section-header">Prediction Results<span class="section-sub">Based on your inputs</span></div>',
        unsafe_allow_html=True,
    )

    ec1, ec2, ec3 = st.columns([1, 1, 2])
    with ec1:
        if st.button("← Edit Company Basics", use_container_width=True, key="edit_step1"):
            st.session_state.wizard_step = 1
            st.rerun()
    with ec2:
        if st.button("← Edit Funding Metrics", use_container_width=True, key="edit_step2"):
            st.session_state.wizard_step = 2
            st.rerun()

    gc1, gc2 = st.columns([1.2, 1])
    with gc1:
        with st.container(border=True):
            render_html('<div class="chart-title">Survival Probability</div><div class="chart-sub">Estimated probability of not closing</div>')
            st.plotly_chart(render_gauge(survival_prob), use_container_width=True, config={"displayModeBar": False}, key="gauge_main")
            badges_html = risk_badge_html(survival_prob) + f'<span class="outcome-pill">🎯 Predicted: {pred_label.title()}</span>'
            render_html(f'<div>{badges_html}</div>')
    with gc2:
        not_exact = [k for k, (matched, exact) in match_notes.items() if not exact]
        with st.container(border=True):
            render_html('<div class="chart-title">What This Means</div>')
            render_html(
                f'<div class="tip-text">Based on patterns in the historical dataset, the model\'s top predicted '
                f'outcome for a startup with these characteristics is <b>{pred_label.title()}</b>, with an estimated '
                f'<b>{survival_prob*100:.1f}%</b> probability of not closing.</div>'
            )
            if not_exact:
                fields = ", ".join(not_exact)
                render_html(f'<div class="warn-note">⚠️ Some inputs ({fields}) weren\'t seen exactly during training — the closest known match was used instead.</div>')

    st.markdown(
        '<div class="section-header">Deep-Dive Analytics<span class="section-sub">Understanding the prediction</span></div>',
        unsafe_allow_html=True,
    )

    dc1, dc2 = st.columns(2)
    with dc1:
        with st.container(border=True):
            render_html('<div class="chart-title">Outcome Probability Breakdown</div><div class="chart-sub">All 4 possible outcomes</div>')
            st.plotly_chart(render_class_probability_chart(prob_by_label), use_container_width=True, config={"displayModeBar": False}, key="prob_breakdown")
    with dc2:
        with st.container(border=True):
            render_html('<div class="chart-title">Feature Importance</div><div class="chart-sub">What drives predictions in this model</div>')
            fi_fig = render_feature_importance(model)
            if fi_fig:
                st.plotly_chart(fi_fig, use_container_width=True, config={"displayModeBar": False}, key="feature_importance")
            else:
                st.info("This model type doesn't expose feature importances directly.")

    with st.container(border=True):
        render_html('<div class="chart-title">🎛️ Scenario Simulator</div><div class="chart-sub">Adjust the sliders to see how the prediction changes</div>')
        sim_funding = st.slider(
            "Total Funding ($M)", 0.0, max(50.0, fd.get("funding_total", 1.0) * 3), float(fd.get("funding_total", 1.0)),
            key="sim_funding",
        )
        sim_rounds = st.slider("Funding Rounds", 0, 10, int(fd.get("funding_rounds", 1)), key="sim_rounds")
        sim_fd = dict(fd)
        sim_fd["funding_total"] = sim_funding
        sim_fd["funding_rounds"] = sim_rounds
        sim_vector, _ = build_feature_vector(sim_fd, encoders, scaler)
        _, _, sim_survival = get_prediction(model, encoders, sim_vector)
        st.plotly_chart(render_gauge(sim_survival), use_container_width=True, config={"displayModeBar": False}, key="gauge_sim")

    st.markdown(
        '<div class="section-header">Next Steps<span class="section-sub">Automated guidance based on your result</span></div>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        for icon, text in generate_tips(fd, pred_label, survival_prob):
            render_html(f'<div class="tip-card"><div class="tip-icon">{icon}</div><div class="tip-text">{text}</div></div>')

    report_text = (
        "STARTUP OUTCOME PREDICTION REPORT\n"
        f"Generated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}\n\n"
        f"Category: {fd.get('category')} (matched: {match_notes['industry'][0]})\n"
        f"Country: {fd.get('country')} (matched: {match_notes['country'][0]})\n"
        f"Region: {fd.get('region')} (matched: {match_notes['region'][0]})\n"
        f"City: {fd.get('city')} (matched: {match_notes['city'][0]})\n"
        f"Founded: {fd.get('founded_year')}\n"
        f"Total Funding: ${fd.get('funding_total')}M\n"
        f"Funding Rounds: {fd.get('funding_rounds')}\n\n"
        "PREDICTION\n"
        f"Predicted Outcome: {pred_label.title()}\n"
        f"Survival Probability (not closing): {survival_prob*100:.1f}%\n"
        f"Full breakdown: {', '.join(f'{k.title()}: {v*100:.1f}%' for k, v in prob_by_label.items())}\n\n"
        "This report is generated from a machine learning model trained on historical\n"
        "startup data and is intended for educational purposes only, not financial advice.\n"
    )
    st.download_button(
        "📄 Export Report (.txt)", data=report_text, file_name="startup_prediction_report.txt", use_container_width=True
    )

    if st.button("🔄 Start New Prediction", use_container_width=True):
        st.session_state.wizard_step = 1
        st.session_state.form_data = {}
        st.session_state.prediction_result = None
        st.rerun()


def main():
    inject_custom_css()
    render_sidebar()

    render_html(
        """
        <div class="hero-eyebrow">🤖 AI-POWERED PREDICTION</div>
        <div class="hero-title">Startup Success Prediction</div>
        <div class="hero-subtitle">Answer a few questions about your startup to get a data-driven outcome estimate.</div>
        """
    )

    model, encoders, scaler = load_artifacts()
    if model is None or encoders is None or scaler is None:
        st.stop()

    step = st.session_state.wizard_step

    if step <= 3:
        render_progress_tracker(step)

    if step == 1:
        render_step_1(encoders)
    elif step == 2:
        render_step_2()
    elif step == 3:
        render_step_3(model, encoders, scaler)
    elif step == 4:
        render_step_4(model, encoders, scaler)


if __name__ == "__main__":
    main()