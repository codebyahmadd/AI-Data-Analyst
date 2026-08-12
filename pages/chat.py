import streamlit as st

st.success("🔥 NEW CHAT.PY IS LOADED")

from utils.ai_chat import answer_question


def show_chat(df):
    """
    Display a professional AI chat interface
    for asking questions about the uploaded dataset.
    """

    # =========================================================
    # PROFESSIONAL HEADER
    # =========================================================

    st.subheader("🤖 AI Data Analyst")

    st.caption(
        "Ask questions about your uploaded dataset "
        "and get instant, data-driven answers."
    )

    st.divider()

    # =========================================================
    # CHAT HISTORY
    # =========================================================

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # =========================================================
    # CLEAR CHAT
    # =========================================================

    clear_col1, clear_col2 = st.columns([5, 1])

    with clear_col2:

        if st.button(
            "🧹 Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []
            st.rerun()

    # =========================================================
    # EXAMPLE QUESTIONS
    # =========================================================

    st.markdown("### 💡 Explore Your Data")

    st.caption(
        "Choose a question below or type your own question."
    )

    # ---------------------------------------------------------
    # DATASET QUESTIONS
    # ---------------------------------------------------------

    with st.expander(
        "📊 Dataset Overview",
        expanded=True
    ):

        overview_questions = [
            "How many rows are in the dataset?",
            "How many columns are in the dataset?",
            "What are the column names?",
            "What are the numeric columns?",
            "What are the categorical columns?",
        ]

        for question in overview_questions:

            if st.button(
                question,
                key=f"overview_{question}",
                use_container_width=True
            ):

                st.session_state.selected_question = question

    # ---------------------------------------------------------
    # DATA QUALITY QUESTIONS
    # ---------------------------------------------------------

    with st.expander(
        "🧹 Data Quality"
    ):

        quality_questions = [
            "Are there any missing values?",
            "Are there any duplicate rows?",
        ]

        for question in quality_questions:

            if st.button(
                question,
                key=f"quality_{question}",
                use_container_width=True
            ):

                st.session_state.selected_question = question

    # ---------------------------------------------------------
    # SALES QUESTIONS
    # ---------------------------------------------------------

    with st.expander(
        "💰 Sales Analysis"
    ):

        sales_questions = [
            "What is the total sales?",
            "What is the average sales?",
            "What is the highest sales?",
            "What is the lowest sales?",
            "What product has the highest revenue?",
            "What is the best selling product?",
            "What is the best selling category?",
        ]

        for question in sales_questions:

            if st.button(
                question,
                key=f"sales_{question}",
                use_container_width=True
            ):

                st.session_state.selected_question = question

    # ---------------------------------------------------------
    # NUMERIC QUESTIONS
    # ---------------------------------------------------------

    with st.expander(
        "🔢 Statistical Questions"
    ):

        statistical_questions = [
            "What is the average price?",
            "What is the highest quantity?",
        ]

        for question in statistical_questions:

            if st.button(
                question,
                key=f"stats_{question}",
                use_container_width=True
            ):

                st.session_state.selected_question = question

    st.divider()

    # =========================================================
    # CHAT HISTORY DISPLAY
    # =========================================================

    st.markdown("### 💬 Conversation")

    if not st.session_state.chat_history:

        st.info(
            "👋 No questions asked yet. "
            "Choose a quick question above or ask something below."
        )

    else:

        for message in st.session_state.chat_history:

            with st.chat_message(
                message["role"]
            ):

                st.write(
                    message["content"]
                )

    # =========================================================
    # QUESTION INPUT
    # =========================================================

    question = st.chat_input(
        "Ask anything about your dataset..."
    )

    # =========================================================
    # QUICK QUESTION HANDLER
    # =========================================================

    selected_question = st.session_state.get(
        "selected_question"
    )

    if selected_question:

        question = selected_question

        st.session_state.selected_question = None

    # =========================================================
    # PROCESS QUESTION
    # =========================================================

    if question:

        # -----------------------------------------------------
        # USER MESSAGE
        # -----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # -----------------------------------------------------
        # AI ANALYSIS
        # -----------------------------------------------------

        with st.spinner(
            "🤖 Analyzing your dataset..."
        ):

            response = answer_question(
                df,
                question
            )

        # -----------------------------------------------------
        # AI MESSAGE
        # -----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()