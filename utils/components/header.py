import streamlit as st


def show_header():
    """
    Display the application header.
    """

    st.markdown("## 🤖 AI Data Analyst")

    st.markdown(
        """
        **AI-Powered Data Analysis Platform**

        Transform your data into meaningful insights, interactive
        visualizations, forecasts, and AI-powered analysis.
        """
    )

    feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

    with feature_col1:
        st.info("📊 **Data Analysis**")

    with feature_col2:
        st.info("📈 **Interactive Visualizations**")

    with feature_col3:
        st.info("🤖 **AI Insights**")

    with feature_col4:
        st.info("💬 **Chat with Data**")

    st.success(
        "🚀 **Ready to analyze?** Upload a CSV dataset below to get started."
    )

    st.divider()