import streamlit as st

from utils.ai_insights import generate_insights


def show_insights(df):
    """
    Display AI generated insights.
    """

    st.subheader("🤖 AI Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.info(insight)