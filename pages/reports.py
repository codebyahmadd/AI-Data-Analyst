import streamlit as st

from utils.ai_insights import generate_insights
from reports.report_generator import generate_report
from reports.pdf_report import generate_pdf_report


def show_reports(df):
    """
    Display downloadable analysis reports.
    """

    st.subheader("📄 Reports")

    st.caption(
        "Generate and download professional reports "
        "based on your uploaded dataset."
    )

    # -----------------------------
    # Generate Insights
    # -----------------------------
    insights = generate_insights(df)

    # -----------------------------
    # Generate Text Report
    # -----------------------------
    report = generate_report(
        df,
        insights
    )

    # -----------------------------
    # Generate PDF Report
    # -----------------------------
    pdf_report = generate_pdf_report(
        df,
        insights
    )

    # -----------------------------
    # Report Preview
    # -----------------------------
    st.subheader("📋 Report Preview")

    with st.expander("View Report Content"):
        st.text(report)

    st.divider()

    # -----------------------------
    # Download Reports
    # -----------------------------
    st.subheader("📥 Download Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📄 Download TXT Report",
            data=report,
            file_name="AI_Data_Analysis_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            label="📕 Download PDF Report",
            data=pdf_report,
            file_name="AI_Data_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )