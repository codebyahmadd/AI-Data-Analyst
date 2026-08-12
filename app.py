import streamlit as st

from utils.data_loader import load_csv

from utils.components.header import show_header
from utils.components.sidebar import show_sidebar

from pages.overview import show_overview
from pages.visualization import show_visualization
from pages.insights import show_insights
from pages.reports import show_reports
from pages.chat import show_chat


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Professional Dark Theme
# -----------------------------

st.markdown("""
<style>

    /* =========================
       GLOBAL APPLICATION
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                #172033 0%,
                #0E1117 40%,
                #0E1117 100%
            );
        color: #F5F7FA;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background-color: #0B0F14;
        border-right: 1px solid #242B35;
    }

    [data-testid="stSidebar"] * {
        color: #E6EDF3;
    }

    [data-testid="stSidebar"] hr {
        border-color: #242B35;
    }


    /* =========================
       HEADINGS
       ========================= */

    h1 {
        color: #F8FAFC;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #F1F5F9;
        font-weight: 750;
    }

    h3 {
        color: #E2E8F0;
        font-weight: 700;
    }


    /* =========================
       CAPTIONS
       ========================= */

    .stCaption {
        color: #94A3B8;
    }


    /* =========================
       UPLOAD SECTION
       ========================= */

    [data-testid="stFileUploader"] {
        background: linear-gradient(
            145deg,
            #161B22,
            #11161D
        );

        border: 1px solid #30363D;
        border-radius: 16px;
        padding: 18px;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.25);

        transition: all 0.25s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #4F8CFF;

        box-shadow:
            0 10px 35px rgba(79, 140, 255, 0.10);
    }


    /* =========================
       ALERT / SUCCESS MESSAGE
       ========================= */

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #30363D;
    }


    /* =========================
       TABS
       ========================= */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;

        background: #11161D;

        padding: 7px;

        border: 1px solid #242B35;
        border-radius: 14px;

        box-shadow:
            0 6px 20px rgba(0, 0, 0, 0.20);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;

        border-radius: 10px;

        padding: 10px 18px;

        color: #94A3B8;

        font-weight: 600;

        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #1A2230;
        color: #F8FAFC;
    }

    .stTabs [aria-selected="true"] {
        background: #1D4ED8;
        color: white;
    }

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.8rem;
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        border-radius: 10px;

        border: 1px solid #30363D;

        background: #161B22;

        color: #F8FAFC;

        font-weight: 600;

        padding: 8px 18px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #4F8CFF;
        background: #1A2230;
        color: white;

        transform: translateY(-1px);
    }


    /* =========================
       METRIC CARDS
       ========================= */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #161B22,
                #11161D
            );

        border: 1px solid #30363D;

        padding: 18px;

        border-radius: 14px;

        box-shadow:
            0 6px 20px rgba(0, 0, 0, 0.20);

        transition: all 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        border-color: #4F8CFF;

        transform: translateY(-2px);

        box-shadow:
            0 10px 25px rgba(79, 140, 255, 0.08);
    }


    /* =========================
       DATAFRAME
       ========================= */

    [data-testid="stDataFrame"] {
        border: 1px solid #30363D;
        border-radius: 12px;

        overflow: hidden;
    }


    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color: #242B35;
    }


    /* =========================
       SELECTBOX / INPUTS
       ========================= */

    div[data-baseweb="select"] > div {
        background-color: #161B22;
        border-color: #30363D;
        border-radius: 10px;
    }


    /* =========================
       SLIDER
       ========================= */

    [data-testid="stSlider"] {
        padding-top: 8px;
        padding-bottom: 8px;
    }


    /* =========================
       EXPANDERS
       ========================= */

    [data-testid="stExpander"] {
        background-color: #11161D;
        border: 1px solid #30363D;
        border-radius: 12px;
    }


    /* =========================
       TEXT INPUT
       ========================= */

    input,
    textarea {
        background-color: #161B22 !important;
        color: #F8FAFC !important;
        border-color: #30363D !important;
        border-radius: 10px !important;
    }


    /* =========================
       HERO HEADER
       ========================= */

    .hero-header {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172554 50%,
            #0F172A 100%
        );

        border: 1px solid #26354A;

        border-radius: 18px;

        padding: 32px 36px;

        margin-bottom: 20px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.28);
    }


    .hero-badge {
        display: inline-block;

        background: rgba(59, 130, 246, 0.12);

        border: 1px solid rgba(96, 165, 250, 0.35);

        color: #93C5FD;

        padding: 6px 12px;

        border-radius: 999px;

        font-size: 12px;

        font-weight: 700;

        letter-spacing: 0.8px;

        margin-bottom: 12px;
    }


    .hero-header h1 {
        font-size: 42px;

        font-weight: 800;

        margin: 0 0 10px 0;

        color: #F8FAFC;
    }


    .hero-subtitle {
        font-size: 17px;

        line-height: 1.6;

        color: #CBD5E1;

        max-width: 850px;

        margin-bottom: 22px;
    }


    .hero-features {
        display: flex;

        flex-wrap: wrap;

        gap: 10px;
    }


    .hero-features span {
        background: rgba(255, 255, 255, 0.05);

        border: 1px solid #334155;

        color: #CBD5E1;

        padding: 7px 12px;

        border-radius: 8px;

        font-size: 13px;

        font-weight: 600;
    }


    .upload-hint {
        background: linear-gradient(
            90deg,
            rgba(30, 64, 175, 0.20),
            rgba(37, 99, 235, 0.08)
        );

        border: 1px solid rgba(59, 130, 246, 0.25);

        border-radius: 12px;

        padding: 14px 18px;

        color: #CBD5E1;

        margin-bottom: 18px;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header & Sidebar
# -----------------------------

show_header()
show_sidebar()


# -----------------------------
# Upload Section
# -----------------------------

st.header("📂 Upload Your CSV File")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    df = load_csv(uploaded_file)

    st.success("✅ Dataset loaded successfully.")


    # -----------------------------
    # Professional Tabs
    # -----------------------------

    overview_tab, visualization_tab, insights_tab, reports_tab, chat_tab = st.tabs(
        [
            "📊 Overview",
            "📈 Visualization",
            "🤖 AI Insights",
            "📄 Reports",
            "💬 Chat with Data"
        ]
    )


    with overview_tab:
        show_overview(df)


    with visualization_tab:
        show_visualization(df)


    with insights_tab:
        show_insights(df)


    with reports_tab:
        show_reports(df)


    with chat_tab:
        show_chat(df)