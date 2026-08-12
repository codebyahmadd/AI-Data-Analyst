import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_summary import get_dataset_info
from utils.data_cleaner import clean_data

from utils.statistics import (
    get_dataset_statistics,
    get_column_summary,
    get_missing_report,
)

from utils.health_score import (
    calculate_health_score,
    get_health_status,
)

from utils.chart_generator import create_correlation_heatmap


def show_overview(df):
    """
    Display the complete dataset overview.
    """

    # =========================================================
    # ADVANCED BUSINESS DASHBOARD
    # =========================================================

    st.subheader("🚀 Business Performance Dashboard")

    st.caption(
        "Key business metrics automatically calculated from your dataset."
    )

    # ---------------------------------------------------------
    # Default KPI values
    # ---------------------------------------------------------

    total_revenue = None
    average_sale = None
    total_units = None
    best_product = "N/A"
    best_category = "N/A"

    # ---------------------------------------------------------
    # Detect Quantity + Price
    # ---------------------------------------------------------

    if "Quantity" in df.columns and "Price" in df.columns:

        quantity = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        )

        price = pd.to_numeric(
            df["Price"],
            errors="coerce"
        )

        sales = quantity * price
        valid_sales = sales.dropna()

        if not valid_sales.empty:

            total_revenue = valid_sales.sum()
            average_sale = valid_sales.mean()

        # Total units
        valid_quantity = quantity.dropna()

        if not valid_quantity.empty:
            total_units = valid_quantity.sum()

        # -----------------------------------------------------
        # Best Product
        # -----------------------------------------------------

        if "Product" in df.columns:

            product_data = pd.DataFrame({
                "Product": df["Product"],
                "Quantity": quantity
            })

            product_data = product_data.dropna(
                subset=["Product", "Quantity"]
            )

            if not product_data.empty:

                product_sales = (
                    product_data
                    .groupby("Product")["Quantity"]
                    .sum()
                    .sort_values(ascending=False)
                )

                if not product_sales.empty:
                    best_product = str(
                        product_sales.index[0]
                    )

        # -----------------------------------------------------
        # Best Category
        # -----------------------------------------------------

        if "Category" in df.columns:

            category_data = pd.DataFrame({
                "Category": df["Category"],
                "Quantity": quantity
            })

            category_data = category_data.dropna(
                subset=["Category", "Quantity"]
            )

            if not category_data.empty:

                category_sales = (
                    category_data
                    .groupby("Category")["Quantity"]
                    .sum()
                    .sort_values(ascending=False)
                )

                if not category_sales.empty:
                    best_category = str(
                        category_sales.index[0]
                    )

    # =========================================================
    # KPI CARDS
    # =========================================================

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    # Revenue
    if total_revenue is not None:

        kpi1.metric(
            "💰 Total Revenue",
            f"{total_revenue:,.2f}"
        )

    else:

        kpi1.metric(
            "💰 Total Revenue",
            "N/A"
        )

    # Average Sale
    if average_sale is not None:

        kpi2.metric(
            "📈 Average Sale",
            f"{average_sale:,.2f}"
        )

    else:

        kpi2.metric(
            "📈 Average Sale",
            "N/A"
        )

    # Units
    if total_units is not None:

        kpi3.metric(
            "📦 Units Sold",
            f"{total_units:,.0f}"
        )

    else:

        kpi3.metric(
            "📦 Units Sold",
            "N/A"
        )

    # Best Product
    kpi4.metric(
        "🏆 Best Product",
        best_product
    )

    # Best Category
    kpi5.metric(
        "🏷️ Top Category",
        best_category
    )

    st.divider()

    # =========================================================
    # SALES PERFORMANCE CHART
    # =========================================================

    if (
        "Quantity" in df.columns
        and "Price" in df.columns
    ):

        chart_data = df.copy()

        chart_data["Quantity"] = pd.to_numeric(
            chart_data["Quantity"],
            errors="coerce"
        )

        chart_data["Price"] = pd.to_numeric(
            chart_data["Price"],
            errors="coerce"
        )

        chart_data["Sales"] = (
            chart_data["Quantity"]
            * chart_data["Price"]
        )

        chart_data = chart_data.dropna(
            subset=["Sales"]
        )

        if not chart_data.empty:

            st.subheader("📊 Sales Performance")

            # -------------------------------------------------
            # Category Sales
            # -------------------------------------------------

            if "Category" in chart_data.columns:

                category_chart = (
                    chart_data
                    .groupby("Category")["Sales"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .reset_index()
                )

                fig = px.bar(
                    category_chart,
                    x="Category",
                    y="Sales",
                    text_auto=".2s",
                    title="Revenue by Category"
                )

                fig.update_layout(
                    template="plotly_white",
                    title_x=0.5,
                    xaxis_title="Category",
                    yaxis_title="Revenue"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # -------------------------------------------------
            # Product Sales
            # -------------------------------------------------

            elif "Product" in chart_data.columns:

                product_chart = (
                    chart_data
                    .groupby("Product")["Sales"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .head(10)
                    .reset_index()
                )

                fig = px.bar(
                    product_chart,
                    x="Product",
                    y="Sales",
                    text_auto=".2s",
                    title="Top Products by Revenue"
                )

                fig.update_layout(
                    template="plotly_white",
                    title_x=0.5,
                    xaxis_title="Product",
                    yaxis_title="Revenue"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            st.divider()

    # =========================================================
    # DATASET PREVIEW
    # =========================================================

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =========================================================
    # DATASET SUMMARY
    # =========================================================

    st.subheader("📊 Dataset Summary")

    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = int(
        df.isnull().sum().sum()
    )

    memory_usage = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        f"{rows:,}"
    )

    col2.metric(
        "Columns",
        f"{columns:,}"
    )

    col3.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

    col4.metric(
        "Memory (KB)",
        f"{memory_usage:,.2f}"
    )

    st.divider()

    # =========================================================
    # DATASET HEALTH
    # =========================================================

    st.subheader("❤️ Dataset Health")

    health_data = calculate_health_score(df)

    score = health_data["score"]

    status, icon = get_health_status(score)

    health_col1, health_col2, health_col3 = st.columns(3)

    health_col1.metric(
        "Health Score",
        f"{score}/100"
    )

    health_col2.metric(
        "Status",
        f"{icon} {status}"
    )

    health_col3.metric(
        "Duplicate Rows",
        f"{health_data['duplicate_count']:,}"
    )

    st.progress(
        score / 100,
        text=f"Dataset Health: {score}%"
    )

    st.caption(
        f"Missing data: {health_data['missing_percentage']}% "
        f"| Duplicate rows: "
        f"{health_data['duplicate_percentage']}%"
    )

    st.divider()

    # =========================================================
    # COLUMN TYPE SUMMARY
    # =========================================================

    st.subheader("🔢 Column Type Summary")

    column_summary = get_column_summary(df)

    type_col1, type_col2, type_col3 = st.columns(3)

    type_col1.metric(
        "Numeric Columns",
        column_summary["Numeric"]
    )

    type_col2.metric(
        "Categorical Columns",
        column_summary["Categorical"]
    )

    type_col3.metric(
        "Datetime Columns",
        column_summary["Datetime"]
    )

    st.divider()

    # =========================================================
    # MISSING VALUE REPORT
    # =========================================================

    st.subheader("🚨 Missing Value Report")

    missing_report = get_missing_report(df)

    st.dataframe(
        missing_report,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =========================================================
    # STATISTICAL SUMMARY
    # =========================================================

    st.subheader("📈 Statistical Summary")

    statistics = get_dataset_statistics(df)

    if statistics is not None:

        st.dataframe(
            statistics,
            use_container_width=True
        )

    else:

        st.info(
            "No numeric columns are available "
            "for statistical analysis."
        )

    st.divider()

    # =========================================================
    # CORRELATION ANALYSIS
    # =========================================================

    st.subheader("🔗 Correlation Analysis")

    correlation_fig = create_correlation_heatmap(df)

    if correlation_fig is not None:

        st.plotly_chart(
            correlation_fig,
            use_container_width=True
        )

    else:

        st.info(
            "Correlation analysis requires at least "
            "two numeric columns."
        )

    st.divider()

    # =========================================================
    # DATASET INFORMATION
    # =========================================================

    st.subheader("📑 Dataset Information")

    dataset_info = get_dataset_info(df)

    st.dataframe(
        dataset_info,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =========================================================
    # DATA CLEANING
    # =========================================================

    st.subheader("🧹 Data Cleaning")

    st.caption(
        "Clean your dataset by removing duplicate rows "
        "and handling missing values."
    )

    clean_button = st.button(
        "🧹 Clean Dataset",
        use_container_width=False
    )

    if clean_button:

        original_df = df.copy()

        cleaned_df = clean_data(df)

        original_rows = len(original_df)
        cleaned_rows = len(cleaned_df)

        original_missing = int(
            original_df.isnull().sum().sum()
        )

        cleaned_missing = int(
            cleaned_df.isnull().sum().sum()
        )

        original_duplicates = int(
            original_df.duplicated().sum()
        )

        cleaned_duplicates = int(
            cleaned_df.duplicated().sum()
        )

        duplicates_removed = (
            original_duplicates
            - cleaned_duplicates
        )

        missing_values_handled = (
            original_missing
            - cleaned_missing
        )

        st.success(
            "✅ Dataset cleaned successfully."
        )

        # =====================================================
        # CLEANING SUMMARY
        # =====================================================

        st.markdown("### 📊 Cleaning Summary")

        summary_col1, summary_col2, summary_col3, summary_col4 = (
            st.columns(4)
        )

        summary_col1.metric(
            "Original Rows",
            f"{original_rows:,}"
        )

        summary_col2.metric(
            "Cleaned Rows",
            f"{cleaned_rows:,}"
        )

        summary_col3.metric(
            "Duplicates Removed",
            f"{duplicates_removed:,}"
        )

        summary_col4.metric(
            "Missing Values Handled",
            f"{missing_values_handled:,}"
        )

        st.divider()

        # =====================================================
        # BEFORE VS AFTER
        # =====================================================

        st.markdown(
            "### 🔄 Before vs After Cleaning"
        )

        comparison_col1, comparison_col2 = (
            st.columns(2)
        )

        with comparison_col1:

            st.markdown(
                "#### 🔴 Before Cleaning"
            )

            st.write(
                f"**Rows:** {original_rows:,}"
            )

            st.write(
                f"**Missing Values:** "
                f"{original_missing:,}"
            )

            st.write(
                f"**Duplicate Rows:** "
                f"{original_duplicates:,}"
            )

        with comparison_col2:

            st.markdown(
                "#### 🟢 After Cleaning"
            )

            st.write(
                f"**Rows:** {cleaned_rows:,}"
            )

            st.write(
                f"**Missing Values:** "
                f"{cleaned_missing:,}"
            )

            st.write(
                f"**Duplicate Rows:** "
                f"{cleaned_duplicates:,}"
            )

        st.divider()

        # =====================================================
        # CLEANING ACTIONS
        # =====================================================

        st.markdown(
            "### 🧹 Cleaning Actions"
        )

        if duplicates_removed > 0:

            st.success(
                f"✅ Removed "
                f"{duplicates_removed:,} "
                f"duplicate row(s)."
            )

        else:

            st.info(
                "✓ No duplicate rows were found."
            )

        if missing_values_handled > 0:

            st.success(
                f"✅ Handled "
                f"{missing_values_handled:,} "
                f"missing value(s)."
            )

        else:

            st.info(
                "✓ No missing values were found."
            )

        st.divider()

        # =====================================================
        # CLEANED DATASET PREVIEW
        # =====================================================

        st.markdown(
            "### 👀 Cleaned Dataset Preview"
        )

        st.dataframe(
            cleaned_df.head(),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # =====================================================
        # DOWNLOAD CLEANED DATASET
        # =====================================================

        st.markdown(
            "### 📥 Download Cleaned Dataset"
        )

        csv_data = cleaned_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )