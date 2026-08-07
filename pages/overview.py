import streamlit as st

from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data
from utils.statistics import (
    get_dataset_statistics,
    get_column_summary,
    get_missing_report,
)
from utils.health_score import (
    calculate_health_score,
    get_health_status,
)
from utils.chart_generator import create_correlation_heatmap


def show_overview(df):
    """
    Display the complete dataset overview.
    """

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

    memory_usage = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", columns)
    col3.metric("Missing Values", missing_values)
    col4.metric("Memory (KB)", memory_usage)

    st.divider()

    # -----------------------------
    # Dataset Health
    # -----------------------------
    st.subheader("❤️ Dataset Health")

    health_data = calculate_health_score(df)

    score = health_data["score"]
    status, icon = get_health_status(score)

    health_col1, health_col2, health_col3 = st.columns(3)

    health_col1.metric(
        "Health Score",
        f"{score}/100"
    )

    health_col2.metric(
        "Status",
        f"{icon} {status}"
    )

    health_col3.metric(
        "Duplicate Rows",
        health_data["duplicate_count"]
    )

    st.progress(
        score / 100,
        text=f"Dataset Health: {score}%"
    )

    st.caption(
        f"Missing data: {health_data['missing_percentage']}% "
        f"| Duplicate rows: "
        f"{health_data['duplicate_percentage']}%"
    )

    st.divider()

    # -----------------------------
    # Column Summary
    # -----------------------------
    st.subheader("🔢 Column Type Summary")

    column_summary = get_column_summary(df)

    type_col1, type_col2, type_col3 = st.columns(3)

    type_col1.metric(
        "Numeric Columns",
        column_summary["Numeric"]
    )

    type_col2.metric(
        "Categorical Columns",
        column_summary["Categorical"]
    )

    type_col3.metric(
        "Datetime Columns",
        column_summary["Datetime"]
    )

    st.divider()

    # -----------------------------
    # Missing Value Report
    # -----------------------------
    st.subheader("🚨 Missing Value Report")

    missing_report = get_missing_report(df)

    st.dataframe(
        missing_report,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # Statistical Summary
    # -----------------------------
    st.subheader("📈 Statistical Summary")

    statistics = get_dataset_statistics(df)

    if statistics is not None:
        st.dataframe(
            statistics,
            use_container_width=True
        )
    else:
        st.info(
            "No numeric columns are available "
            "for statistical analysis."
        )

    st.divider()

    # -----------------------------
    # Correlation Analysis
    # -----------------------------
    st.subheader("🔗 Correlation Analysis")

    correlation_fig = create_correlation_heatmap(df)

    if correlation_fig is not None:
        st.plotly_chart(
            correlation_fig,
            use_container_width=True
        )
    else:
        st.info(
            "Correlation analysis requires at least "
            "two numeric columns."
        )

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

        st.success(
            "✅ Dataset cleaned successfully."
        )

        st.dataframe(
            cleaned_df.head(),
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # Download Cleaned Dataset
        # -----------------------------
        csv_data = cleaned_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )