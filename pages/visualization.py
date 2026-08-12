import streamlit as st
import pandas as pd
import plotly.express as px

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


def parse_date_series(series):
    """
    Safely convert a column into datetime values.

    Handles:
    - Normal date strings
    - Excel serial dates
    - Unix timestamps
    """

    # Numeric date values
    if pd.api.types.is_numeric_dtype(series):

        numeric = pd.to_numeric(series, errors="coerce")

        valid = numeric.dropna()

        if valid.empty:
            return pd.Series(pd.NaT, index=series.index)

        median_value = valid.median()

        # Excel serial date
        if 20000 <= median_value <= 60000:
            return pd.to_datetime(
                numeric,
                unit="D",
                origin="1899-12-30",
                errors="coerce"
            )

        # Unix timestamp in seconds
        if 1_000_000_000 <= median_value <= 2_000_000_000:
            return pd.to_datetime(
                numeric,
                unit="s",
                errors="coerce"
            )

        # Do not treat small arbitrary numbers as dates
        return pd.Series(pd.NaT, index=series.index)

    # Text/object dates
    return pd.to_datetime(
        series,
        errors="coerce",
        format="mixed"
    )


def detect_date_column(df):
    """
    Automatically detect a suitable date column.
    """

    common_date_names = [
        "Date",
        "date",
        "Order Date",
        "order_date",
        "Transaction Date",
        "transaction_date",
        "Sales Date",
        "sales_date",
        "Invoice Date",
        "invoice_date",
    ]

    # First check commonly named date columns
    for column in common_date_names:

        if column in df.columns:

            converted = parse_date_series(df[column])

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.5:
                return column

    # Then check only non-numeric columns
    # to avoid treating Quantity/Price as dates.
    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):
            continue

        converted = parse_date_series(df[column])

        valid_ratio = converted.notna().mean()

        if valid_ratio >= 0.5:
            return column

    return None


def create_sales_dataframe(df):
    """
    Create a dataframe containing Date and Sales.
    Sales = Quantity × Price
    """

    date_column = detect_date_column(df)

    if date_column is None:
        return None, None

    if (
        "Quantity" not in df.columns
        or "Price" not in df.columns
    ):
        return None, date_column

    sales_df = df.copy()

    sales_df["Date"] = parse_date_series(
    sales_df[date_column]
    )

    sales_df["Quantity"] = pd.to_numeric(
        sales_df["Quantity"],
        errors="coerce"
    )

    sales_df["Price"] = pd.to_numeric(
        sales_df["Price"],
        errors="coerce"
    )

    sales_df["Sales"] = (
        sales_df["Quantity"]
        * sales_df["Price"]
    )

    sales_df = sales_df.dropna(
        subset=["Date", "Sales"]
    )

    return sales_df, date_column


def show_sales_forecast(df):
    """
    Display sales trend and simple future sales forecast.
    """

    st.subheader("🔮 Sales Trend & Forecast")

    st.caption(
        "Analyze historical sales performance and estimate "
        "future sales based on the available time-series data."
    )

    sales_df, date_column = create_sales_dataframe(df)

    # =====================================================
    # VALIDATION
    # =====================================================

    if date_column is None:

        st.info(
            "📅 No suitable date column was detected. "
            "Forecasting requires a date column."
        )

        return

    if sales_df is None:

        st.warning(
            "⚠️ Forecasting requires both "
            "`Quantity` and `Price` columns."
        )

        return

    if sales_df.empty:

        st.warning(
            "⚠️ No valid date and sales records are available "
            "for forecasting."
        )

        return

    # =====================================================
    # DATE RANGE
    # =====================================================

    min_date = sales_df["Date"].min()
    max_date = sales_df["Date"].max()

    st.write(
        f"📅 **Data period:** "
        f"{min_date.strftime('%Y-%m-%d')} "
        f"to "
        f"{max_date.strftime('%Y-%m-%d')}"
    )

    # =====================================================
    # AGGREGATE SALES
    # =====================================================

    daily_sales = (
        sales_df
        .groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    if len(daily_sales) < 2:

        st.warning(
            "⚠️ At least two different dates are required "
            "for trend analysis."
        )

        return

    # =====================================================
    # SALES TREND
    # =====================================================

    st.markdown("### 📈 Historical Sales Trend")

    trend_fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        markers=True,
        title="Sales Over Time"
    )

    trend_fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # FORECAST SETTINGS
    # =====================================================

    st.markdown("### ⚙️ Forecast Settings")

    forecast_days = st.slider(
        "Select Forecast Period",
        min_value=7,
        max_value=30,
        value=7,
        step=1
    )

    # =====================================================
    # SIMPLE MOVING AVERAGE FORECAST
    # =====================================================

    # Use recent observations
    window_size = min(
        7,
        len(daily_sales)
    )

    recent_sales = (
        daily_sales["Sales"]
        .tail(window_size)
    )

    average_sales = recent_sales.mean()

    last_date = daily_sales["Date"].max()

    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq="D"
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast": [average_sales] * forecast_days
    })

    # =====================================================
    # FORECAST CHART
    # =====================================================

    st.markdown("### 🔮 Sales Forecast")

    historical_plot = daily_sales[
        ["Date", "Sales"]
    ].copy()

    historical_plot["Type"] = "Historical"

    forecast_plot = forecast_df[
        ["Date", "Forecast"]
    ].copy()

    forecast_plot = forecast_plot.rename(
        columns={
            "Forecast": "Sales"
        }
    )

    forecast_plot["Type"] = "Forecast"

    combined_df = pd.concat(
        [
            historical_plot,
            forecast_plot
        ],
        ignore_index=True
    )

    forecast_fig = px.line(
        combined_df,
        x="Date",
        y="Sales",
        color="Type",
        markers=True,
        title="Historical Sales & Future Forecast"
    )

    forecast_fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

    # =====================================================
    # FORECAST KPI
    # =====================================================

    total_forecast = (
        forecast_df["Forecast"].sum()
    )

    average_forecast = (
        forecast_df["Forecast"].mean()
    )

    forecast_col1, forecast_col2 = st.columns(2)

    forecast_col1.metric(
        "🔮 Forecasted Sales",
        f"{total_forecast:,.2f}"
    )

    forecast_col2.metric(
        "📊 Expected Daily Sales",
        f"{average_forecast:,.2f}"
    )

    st.divider()

    # =====================================================
    # FORECAST TABLE
    # =====================================================

    st.markdown("### 📋 Forecast Details")

    display_forecast = forecast_df.copy()

    display_forecast["Date"] = (
        display_forecast["Date"]
        .dt.strftime("%Y-%m-%d")
    )

    display_forecast["Forecast"] = (
        display_forecast["Forecast"]
        .round(2)
    )

    st.dataframe(
        display_forecast,
        use_container_width=True,
        hide_index=True
    )


def show_visualization(df):
    """
    Display all data visualizations.
    """

    st.subheader("📊 Advanced Data Visualization")

    st.caption(
        "Explore your dataset using interactive charts "
        "and sales forecasting."
    )

    # =====================================================
    # SALES TREND & FORECAST
    # =====================================================

    show_sales_forecast(df)

    st.divider()

    # =====================================================
    # CHART SELECTOR
    # =====================================================

    st.subheader("📊 Custom Data Visualization")

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

    # =====================================================
    # BAR CHART
    # =====================================================

    if chart_type == "Bar Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="bar"
            )

            fig = create_bar_chart(
                df,
                column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No suitable categorical columns found."
            )

    # =====================================================
    # PIE CHART
    # =====================================================

    elif chart_type == "Pie Chart":

        if categorical_columns:

            column = st.selectbox(
                "Select Column",
                categorical_columns,
                key="pie"
            )

            fig = create_pie_chart(
                df,
                column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No suitable categorical columns found."
            )

    # =====================================================
    # LINE CHART
    # =====================================================

    elif chart_type == "Line Chart":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="line"
            )

            fig = create_line_chart(
                df,
                column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numeric columns found."
            )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    elif chart_type == "Histogram":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="hist"
            )

            fig = create_histogram(
                df,
                column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numeric columns found."
            )

    # =====================================================
    # SCATTER PLOT
    # =====================================================

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
                "Scatter Plot requires at least "
                "two numeric columns."
            )

    # =====================================================
    # BOX PLOT
    # =====================================================

    elif chart_type == "Box Plot":

        if numeric_columns:

            column = st.selectbox(
                "Select Numeric Column",
                numeric_columns,
                key="box"
            )

            fig = create_box_plot(
                df,
                column
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.warning(
                "No numeric columns found."
            )