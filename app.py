import streamlit as st

from utils.data_loader import load_csv

from utils.components.header import show_header
from utils.components.sidebar import show_sidebar

from pages.overview import show_overview
from pages.visualization import show_visualization
from pages.insights import show_insights
from pages.reports import show_reports


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)

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
    overview_tab, visualization_tab, insights_tab, reports_tab = st.tabs(
        [
            "📊 Overview",
            "📈 Visualization",
            "🤖 AI Insights",
            "📄 Reports"
        ]
    )

    with overview_tab:
        show_overview(df)

    with visualization_tab:
        show_visualization(df)

    with insights_tab:
        show_insights(df)

    with reports_tab:
        show_reports()