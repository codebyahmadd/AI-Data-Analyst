import streamlit as st

from utils.data_loader import load_csv

from utils.ai_insights import generate_insights

from utils.components.header import show_header
from utils.components.sidebar import show_sidebar

from pages.overview import show_overview
from pages.visualization import show_visualization


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

    # Load Dataset
    df = load_csv(uploaded_file)

    st.success("✅ Dataset loaded successfully.")

    # -----------------------------
    # Overview
    # -----------------------------
    show_overview(df)

    st.divider()

    # -----------------------------
    # Visualization
    # -----------------------------
    show_visualization(df)

    st.divider()

    # -----------------------------
    # AI Insights
    # -----------------------------
    st.subheader("🤖 AI Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.write(insight)