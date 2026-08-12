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

    # =========================================================
    # GENERATE AI INSIGHTS
    # =========================================================

    try:
        insights = generate_insights(df)

    except Exception as e:
        st.error("❌ Unable to generate AI insights.")
        st.exception(e)
        return

    # ---------------------------------------------------------
    # Make sure insights is always a list
    # ---------------------------------------------------------

    if insights is None:
        insights = []

    elif isinstance(insights, str):
        insights = [insights]

    elif not isinstance(insights, (list, tuple)):
        try:
            insights = list(insights)
        except TypeError:
            insights = [str(insights)]

    else:
        insights = list(insights)

    # =========================================================
    # INSIGHTS SECTION
    # =========================================================

    st.markdown("### 🤖 AI Insights")

    if len(insights) == 0:

        st.info(
            "No automatic insights were generated for this dataset."
        )

    else:

        for index, insight in enumerate(insights, start=1):

            if insight is not None and str(insight).strip():

                st.markdown(
                    f"**{index}.** {str(insight)}"
                )

    st.divider()

    # =========================================================
    # GENERATE TEXT REPORT
    # =========================================================

    try:

        report = generate_report(
            df,
            insights
        )

    except Exception as e:

        st.error("❌ Unable to generate the text report.")
        st.exception(e)
        return

    # =========================================================
    # REPORT PREVIEW
    # =========================================================

    st.markdown("### 📋 Report Preview")

    with st.expander(
        "👀 View Complete Report",
        expanded=False
    ):

        st.code(
            report,
            language="text"
        )

    st.divider()

    # =========================================================
    # GENERATE PDF REPORT
    # =========================================================

    try:

        pdf_report = generate_pdf_report(
            df,
            insights
        )

    except Exception as e:

        pdf_report = None

        st.warning(
            "⚠️ PDF report could not be generated."
        )

        st.caption(
            f"PDF error: {e}"
        )

    # =========================================================
    # DOWNLOAD REPORTS
    # =========================================================

    st.markdown("### 📥 Download Reports")

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # TXT DOWNLOAD
    # ---------------------------------------------------------

    with col1:

        st.download_button(
            label="📄 Download TXT Report",
            data=report,
            file_name="AI_Data_Analysis_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

    # ---------------------------------------------------------
    # PDF DOWNLOAD
    # ---------------------------------------------------------

    with col2:

        if pdf_report is not None:

            st.download_button(
                label="📕 Download PDF Report",
                data=pdf_report,
                file_name="AI_Data_Analysis_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        else:

            st.button(
                "📕 PDF Unavailable",
                disabled=True,
                use_container_width=True
            )

    st.divider()

    # =========================================================
    # REPORT STATUS
    # =========================================================

    st.success(
        f"✅ Report generated successfully with "
        f"{len(insights)} AI insight(s)."
    )