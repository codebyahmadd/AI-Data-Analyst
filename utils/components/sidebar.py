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

        st.progress(20)

        st.caption("Phase 1 of 5 Completed")

        st.markdown("---")

        st.subheader("🚀 Upcoming Features")

        st.write("✅ Interactive Charts")
        st.write("✅ AI Insights")
        st.write("✅ Chat with Data")
        st.write("✅ PDF Reports")
        st.write("✅ Forecasting")

        st.markdown("---")

        st.caption("Version 0.1.0")