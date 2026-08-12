import streamlit as st
print("INSIGHTS_KPI_V2_LOADED")

from utils.ai_insights import generate_insights
from reports.report_generator import generate_report


def show_insights(df):
    """
    Display AI-generated insights and downloadable report.
    """

    st.subheader("🤖 AI Insights")

    st.caption(
        "Automatically generated observations based on the uploaded dataset."
    )

    # ======================================================
    # GENERATE INSIGHTS
    # ======================================================

    insights = generate_insights(df)

    if not insights:
        st.info("No insights are available for this dataset.")
        return

    # ======================================================
    # CALCULATE KPI VALUES
    # ======================================================

    total_sales = None
    average_sales = None
    best_product = None
    best_category = None

    if (
        "Quantity" in df.columns
        and "Price" in df.columns
    ):

        quantity = df["Quantity"].astype(float)
        price = df["Price"].astype(float)

        sales = quantity * price

        total_sales = sales.sum()
        average_sales = sales.mean()

        # ----------------------------------------------
        # BEST PRODUCT
        # ----------------------------------------------

        if "Product" in df.columns:

            product_quantity = (
                df.assign(Quantity=quantity)
                .groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not product_quantity.empty:
                best_product = product_quantity.index[0]

        # ----------------------------------------------
        # BEST CATEGORY
        # ----------------------------------------------

        if "Category" in df.columns:

            category_quantity = (
                df.assign(Quantity=quantity)
                .groupby("Category")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_quantity.empty:
                best_category = category_quantity.index[0]

    # ======================================================
    # KPI CARDS
    # ======================================================

    st.markdown("### 📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if total_sales is not None:
            st.metric(
                "💰 Total Sales",
                f"{total_sales:,.2f}"
            )
        else:
            st.metric(
                "💰 Total Sales",
                "N/A"
            )

    with col2:

        if average_sales is not None:
            st.metric(
                "📈 Average Sales",
                f"{average_sales:,.2f}"
            )
        else:
            st.metric(
                "📈 Average Sales",
                "N/A"
            )

    with col3:

        st.metric(
            "🏆 Best Product",
            str(best_product)
            if best_product is not None
            else "N/A"
        )

    with col4:

        st.metric(
            "🏷️ Best Category",
            str(best_category)
            if best_category is not None
            else "N/A"
        )

    st.divider()

    # ======================================================
    # AI-GENERATED INSIGHTS
    # ======================================================

    st.markdown("### 💡 Detailed Insights")

    for insight in insights:

        if insight.startswith("⚠️"):

            st.warning(insight)

        elif insight.startswith("✅"):

            st.success(insight)

        elif insight.startswith("💡"):

            st.info(insight)

        elif insight.startswith("💰"):

            st.success(insight)

        elif insight.startswith("🏆"):

            st.success(insight)

        elif insight.startswith("💎"):

            st.success(insight)

        elif insight.startswith("🏷️"):

            st.info(insight)

        elif insight.startswith("💵"):

            st.info(insight)

        else:

            st.info(insight)

    st.divider()

    # ======================================================
    # ANALYSIS REPORT
    # ======================================================

    st.subheader("📄 Analysis Report")

    st.caption(
        "Download a text report containing the dataset analysis "
        "and generated insights."
    )

    report = generate_report(
        df,
        insights
    )

    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="AI_Data_Analysis_Report.txt",
        mime="text/plain"
    )