import streamlit as st

from utils.data_loader import load_csv
from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data
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