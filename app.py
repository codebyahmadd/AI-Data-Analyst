import streamlit as st

from utils.data_loader import load_csv
from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data

from utils.chart_generator import (
    get_chart_columns,
    get_numeric_columns,
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
    create_histogram,
    create_scatter_chart,
    create_box_plot,
)

from utils.ai_insights import generate_insights

from utils.components.header import show_header
from utils.components.sidebar import show_sidebar


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
    missing_values = int(df.isnull().sum().sum())
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
    # Advanced Visualization
    # -----------------------------
    st.subheader("📊 Advanced Data Visualization")

    chart_type = st.selectbox(
        "Select Chart",
        [
            "Bar Chart",
            "Pie Chart",
            "Line Chart",
            "Histogram",
            "Scatter Plot",
            "Box Plot",
        ]
    )

    categorical_columns = get_chart_columns(df)
    numeric_columns = get_numeric_columns(df)

    # -------- BAR --------
    if chart_type == "Bar Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="bar"
            )

            fig = create_bar_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No suitable categorical columns found.")

    # -------- PIE --------
    elif chart_type == "Pie Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="pie"
            )

            fig = create_pie_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No suitable categorical columns found.")

    # -------- LINE --------
    elif chart_type == "Line Chart":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="line"
            )

            fig = create_line_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found.")

    # -------- HISTOGRAM --------
    elif chart_type == "Histogram":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="hist"
            )

            fig = create_histogram(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found.")

    # -------- SCATTER --------
    elif chart_type == "Scatter Plot":

        if len(numeric_columns) >= 2:

            x_column = st.selectbox(
                "X-Axis",
                numeric_columns,
                key="scatter_x"
            )

            y_column = st.selectbox(
                "Y-Axis",
                numeric_columns,
                key="scatter_y"
            )

            fig = create_scatter_chart(df, x_column, y_column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Scatter plot requires at least two numeric columns.")

    # -------- BOX --------
    elif chart_type == "Box Plot":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="box"
            )

            fig = create_box_plot(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found.")

    st.divider()

    # -----------------------------
    # AI Insights
    # -----------------------------
    st.subheader("🤖 AI Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.write(insight)