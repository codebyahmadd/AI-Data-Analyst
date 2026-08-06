import streamlit as st

from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data


def show_overview(df):
    """
    Display dataset overview section.
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