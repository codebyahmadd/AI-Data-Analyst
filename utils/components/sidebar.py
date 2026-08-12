import streamlit as st


def show_sidebar():
    """
    Display the application sidebar.
    """

    with st.sidebar:

        st.title("🤖 AI Data Analyst")

        st.markdown("---")

        st.subheader("📌 Project Status")

        st.success("🟢 Application Running")

        st.markdown("---")

        st.subheader("📊 Dashboard Progress")

        st.progress(1.0)

        st.caption("All Core Features Completed")

        st.markdown("---")

        st.subheader("✨ Key Features")

        st.write("✅ Interactive Charts")
        st.write("✅ AI Insights")
        st.write("✅ Chat with Data")
        st.write("✅ PDF Reports")
        st.write("✅ Sales Forecasting")

        st.markdown("---")

        st.caption("Version 1.0.0")