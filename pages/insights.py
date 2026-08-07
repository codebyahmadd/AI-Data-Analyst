import streamlit as st

from utils.ai_insights import generate_insights


def show_insights(df):
    """
    Display AI generated insights.
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