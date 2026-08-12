import streamlit as st


def show_sidebar():
    """
    Display the application sidebar.
    """

    with st.sidebar:

        # -----------------------------
        # Application Branding
        # -----------------------------

        st.markdown("## 🤖 AI Data Analyst")

        st.caption("AI-Powered Data Analysis")

        st.markdown("---")

        # -----------------------------
        # Project Status
        # -----------------------------

        st.subheader("📌 Project Status")

        st.success("🟢 Application Running")

        st.markdown("---")

        # -----------------------------
        # Dashboard Progress
        # -----------------------------

        st.subheader("📊 Dashboard Progress")

        st.progress(1.0)

        st.caption("All Core Features Completed")

        st.markdown("---")

        # -----------------------------
        # Key Features
        # -----------------------------

        st.subheader("✨ Key Features")

        st.write("📊 Interactive Charts")
        st.write("🤖 AI Insights")
        st.write("💬 Chat with Data")
        st.write("📄 PDF Reports")
        st.write("🔮 Sales Forecasting")

        st.markdown("---")

        # -----------------------------
        # Version
        # -----------------------------

        st.caption("AI Data Analyst • Version 1.0.0")