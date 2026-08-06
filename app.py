import streamlit as st

from utils.data_loader import load_csv
from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data
from utils.components.header import show_header
from utils.components.sidebar import show_sidebar
from utils.chart_generator import (
    get_chart_columns,
    create_bar_chart,
    create_pie_chart,
)
from utils.ai_insights import generate_insights

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------
show_header()
show_sidebar()


# -----------------------------
# CSV Upload
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
    # Dataset Preview
    # -----------------------------
    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # Dataset Summary
    # -----------------------------
    st.subheader("📊 Dataset Summary")

    rows = df.shape[0]
    columns = df.shape[1]
    missing_values = df.isnull().sum().sum()
    memory_usage = round(df.memory_usage(deep=True).sum() / 1024, 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", columns)
    col3.metric("Missing Values", missing_values)
    col4.metric("Memory (KB)", memory_usage)

    st.divider()

    # -----------------------------
    # Dataset Information
    # -----------------------------
    st.subheader("📑 Dataset Information")

    dataset_info = get_dataset_info(df)

    st.dataframe(
        dataset_info,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

       # -----------------------------
    # Data Cleaning
    # -----------------------------
    st.subheader("🧹 Data Cleaning")

    if st.button("🧹 Clean Dataset"):

        cleaned_df = clean_data(df)

        st.success("✅ Dataset cleaned successfully.")

        st.dataframe(
            cleaned_df.head(),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # -----------------------------
    # Interactive Charts
    # -----------------------------
    st.subheader("📊 Interactive Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Pie Chart"]
    )

    chart_columns = get_chart_columns(df)

    if  chart_columns:

     column = st.selectbox(
        "Select Column",
        chart_columns
    )

    if chart_type == "Bar Chart":

        fig = create_bar_chart(df, column)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart":

        fig = create_pie_chart(df, column)
        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("⚠️ No suitable columns found for visualization.")
        st.divider()

    # -----------------------------
    # AI Insights
    # -----------------------------
    st.subheader("🤖 AI Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.write(insight)