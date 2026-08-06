import streamlit as st

from utils.chart_generator import (
    get_chart_columns,
    get_numeric_columns,
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
    create_histogram,
    create_scatter_chart,
    create_box_plot,
)


def show_visualization(df):
    """
    Display all data visualizations.
    """

    st.subheader("📊 Advanced Data Visualization")

    chart_type = st.selectbox(
        "Select Chart",
        [
            "Bar Chart",
            "Pie Chart",
            "Line Chart",
            "Histogram",
            "Scatter Plot",
            "Box Plot",
        ]
    )

    categorical_columns = get_chart_columns(df)
    numeric_columns = get_numeric_columns(df)

    # -----------------------------
    # Bar Chart
    # -----------------------------
    if chart_type == "Bar Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="bar"
            )

            fig = create_bar_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No suitable categorical columns found.")

    # -----------------------------
    # Pie Chart
    # -----------------------------
    elif chart_type == "Pie Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="pie"
            )

            fig = create_pie_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No suitable categorical columns found.")

    # -----------------------------
    # Line Chart
    # -----------------------------
    elif chart_type == "Line Chart":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="line"
            )

            fig = create_line_chart(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found.")

    # -----------------------------
    # Histogram
    # -----------------------------
    elif chart_type == "Histogram":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="hist"
            )

            fig = create_histogram(df, column)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found.")

    # -----------------------------
    # Scatter Plot
    # -----------------------------
    elif chart_type == "Scatter Plot":

        if len(numeric_columns) >= 2:

            x_column = st.selectbox(
                "X-Axis",
                numeric_columns,
                key="scatter_x"
            )

            y_column = st.selectbox(
                "Y-Axis",
                numeric_columns,
                key="scatter_y"
            )

            fig = create_scatter_chart(
                df,
                x_column,
                y_column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning(
                "Scatter Plot requires at least two numeric columns."
            )

    # -----------------------------
    # Box Plot
    # -----------------------------
    elif chart_type == "Box Plot":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="box"
            )

            fig = create_box_plot(df, column)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("No numeric columns found.")