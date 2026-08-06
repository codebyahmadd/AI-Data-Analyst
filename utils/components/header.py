import streamlit as st


def show_header():
    """
    Display the application header.
    """

    st.title("🤖 AI Data Analyst")

    st.markdown(
        """
        ### AI-Powered Data Analysis Platform

        Upload your dataset and get instant insights, visualizations,
        and AI-powered recommendations.
        """
    )

    st.info(
        "🚀 Upload a CSV file to start exploring your data."
    )

    st.divider()