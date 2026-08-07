import streamlit as st

from utils.ai_insights import generate_insights
from reports.report_generator import generate_report


def show_insights(df):
    """
    Display AI generated insights and downloadable report.
    """

    st.subheader("🤖 AI Insights")

    st.caption(
        "Automatically generated observations based on the uploaded dataset."
    )

    insights = generate_insights(df)

    if not insights:
        st.info("No insights are available for this dataset.")
        return

    # -----------------------------
    # Display Insights
    # -----------------------------
    for insight in insights:

        if insight.startswith("⚠️"):
            st.warning(insight)

        elif insight.startswith("✅"):
            st.success(insight)

        elif insight.startswith("💡"):
            st.info(insight)

        elif insight.startswith("📈"):
            st.info(insight)

        else:
            st.info(insight)

    st.divider()

    # -----------------------------
    # Analysis Report
    # -----------------------------
    st.subheader("📄 Analysis Report")

    report = generate_report(
        df,
        insights
    )

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="AI_Data_Analysis_Report.txt",
        mime="text/plain"
    )