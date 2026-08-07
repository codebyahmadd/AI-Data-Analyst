import streamlit as st

from utils.ai_insights import generate_insights
from reports.report_generator import generate_report


def show_reports(df):
    """
    Display downloadable analysis reports.
    """

    st.subheader("📄 Reports")

    st.caption(
        "Generate and download an analysis report "
        "based on your uploaded dataset."
    )

    # -----------------------------
    # Generate Insights
    # -----------------------------
    insights = generate_insights(df)

    # -----------------------------
    # Generate Report
    # -----------------------------
    report = generate_report(
        df,
        insights
    )

    # -----------------------------
    # Report Preview
    # -----------------------------
    st.subheader("📋 Report Preview")

    with st.expander("View Report Content"):

        st.text(
            report
        )

    st.divider()

    # -----------------------------
    # Download Report
    # -----------------------------
    st.subheader("📥 Download Report")

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="AI_Data_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )