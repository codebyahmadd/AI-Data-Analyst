import pandas as pd


def generate_insights(df):
    """
    Generate automatic business and data-quality insights
    from the uploaded dataset.

    Always returns a list of insights.
    """

    insights = []

    # ======================================================
    # SAFETY CHECK
    # ======================================================

    if df is None:
        return [
            "⚠️ No dataset is available. Please upload a CSV file first."
        ]

    if df.empty:
        return [
            "⚠️ The uploaded dataset is empty."
        ]

    # ======================================================
    # DATASET OVERVIEW
    # ======================================================

    rows = df.shape[0]
    columns = df.shape[1]

    insights.append(
        f"📊 Dataset contains {rows:,} rows and {columns:,} columns."
    )

    # ======================================================
    # DATA QUALITY
    # ======================================================

    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    total_cells = rows * columns

    if total_cells > 0:
        missing_percentage = (missing / total_cells) * 100
    else:
        missing_percentage = 0

    if missing == 0:
        insights.append(
            "✅ No missing values were found in the dataset."
        )
    else:
        insights.append(
            f"⚠️ The dataset contains {missing:,} missing values "
            f"({missing_percentage:.2f}% of all cells)."
        )

    if duplicates == 0:
        insights.append(
            "✅ No duplicate rows were detected."
        )
    else:
        duplicate_percentage = (
            (duplicates / rows) * 100
            if rows > 0
            else 0
        )

        insights.append(
            f"⚠️ The dataset contains {duplicates:,} duplicate rows "
            f"({duplicate_percentage:.2f}% of records)."
        )

    # ======================================================
    # COLUMN TYPES
    # ======================================================

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if numeric_columns:
        insights.append(
            "🔢 Numeric columns: "
            + ", ".join(map(str, numeric_columns))
        )

    if categorical_columns:
        insights.append(
            "📝 Categorical columns: "
            + ", ".join(map(str, categorical_columns))
        )

    # ======================================================
    # SALES ANALYSIS
    #
    # Sales = Quantity × Price
    # ======================================================

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

            # --------------------------------------------------
            # TOTAL SALES
            # --------------------------------------------------

            total_sales = valid_sales.sum()

            insights.append(
                f"💰 Total sales generated: "
                f"{total_sales:,.2f}."
            )

            # --------------------------------------------------
            # AVERAGE SALES
            # --------------------------------------------------

            average_sales = valid_sales.mean()

            insights.append(
                f"📈 Average sales per record: "
                f"{average_sales:,.2f}."
            )

            # --------------------------------------------------
            # HIGHEST SALE
            # --------------------------------------------------

            highest_sales = valid_sales.max()

            insights.append(
                f"🔝 Highest single-record sale: "
                f"{highest_sales:,.2f}."
            )

            # --------------------------------------------------
            # LOWEST SALE
            # --------------------------------------------------

            lowest_sales = valid_sales.min()

            insights.append(
                f"🔻 Lowest single-record sale: "
                f"{lowest_sales:,.2f}."
            )

            # --------------------------------------------------
            # TRANSACTION CONTRIBUTION
            # --------------------------------------------------

            if total_sales > 0:

                highest_sale_percentage = (
                    highest_sales / total_sales
                ) * 100

                insights.append(
                    f"📌 The highest single transaction "
                    f"represents approximately "
                    f"{highest_sale_percentage:.2f}% "
                    f"of total sales."
                )

        # ==================================================
        # PRODUCT ANALYSIS
        # ==================================================

        if "Product" in df.columns:

            product_data = df.copy()

            product_data["Quantity"] = quantity
            product_data["CalculatedSales"] = sales

            # ----------------------------------------------
            # BEST-SELLING PRODUCT
            # ----------------------------------------------

            product_quantity = (
                product_data
                .dropna(subset=["Product"])
                .groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not product_quantity.empty:

                best_product = product_quantity.index[0]
                best_product_quantity = product_quantity.iloc[0]

                insights.append(
                    f"🏆 Best-selling product: "
                    f"{best_product} "
                    f"({best_product_quantity:,.0f} units sold)."
                )

                # ------------------------------------------
                # TOP 3 PRODUCTS
                # ------------------------------------------

                top_products = product_quantity.head(3)

                if len(top_products) >= 2:

                    top_product_text = ", ".join(
                        [
                            f"{name} ({value:,.0f})"
                            for name, value
                            in top_products.items()
                        ]
                    )

                    insights.append(
                        f"📦 Top products by units sold: "
                        f"{top_product_text}."
                    )

            # ----------------------------------------------
            # HIGHEST-REVENUE PRODUCT
            # ----------------------------------------------

            product_revenue = (
                product_data
                .dropna(subset=["Product"])
                .groupby("Product")["CalculatedSales"]
                .sum()
                .sort_values(ascending=False)
            )

            if not product_revenue.empty:

                top_product = product_revenue.index[0]
                top_product_revenue = product_revenue.iloc[0]

                insights.append(
                    f"💎 Highest-revenue product: "
                    f"{top_product} "
                    f"({top_product_revenue:,.2f} in sales)."
                )

                # ------------------------------------------
                # PRODUCT REVENUE CONTRIBUTION
                # ------------------------------------------

                total_product_revenue = product_revenue.sum()

                if total_product_revenue > 0:

                    revenue_share = (
                        top_product_revenue
                        / total_product_revenue
                    ) * 100

                    insights.append(
                        f"💡 {top_product} contributes "
                        f"{revenue_share:.2f}% of total "
                        f"product revenue."
                    )

        # ==================================================
        # CATEGORY ANALYSIS
        # ==================================================

        if "Category" in df.columns:

            category_data = df.copy()

            category_data["Quantity"] = quantity
            category_data["CalculatedSales"] = sales

            # ----------------------------------------------
            # BEST-SELLING CATEGORY
            # ----------------------------------------------

            category_quantity = (
                category_data
                .dropna(subset=["Category"])
                .groupby("Category")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_quantity.empty:

                best_category = category_quantity.index[0]
                best_category_quantity = category_quantity.iloc[0]

                insights.append(
                    f"🏷️ Best-selling category: "
                    f"{best_category} "
                    f"({best_category_quantity:,.0f} units sold)."
                )

            # ----------------------------------------------
            # HIGHEST-REVENUE CATEGORY
            # ----------------------------------------------

            category_revenue = (
                category_data
                .dropna(subset=["Category"])
                .groupby("Category")["CalculatedSales"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_revenue.empty:

                top_category = category_revenue.index[0]
                top_category_revenue = category_revenue.iloc[0]

                insights.append(
                    f"💵 Highest-revenue category: "
                    f"{top_category} "
                    f"({top_category_revenue:,.2f} in sales)."
                )

                # ------------------------------------------
                # CATEGORY REVENUE CONTRIBUTION
                # ------------------------------------------

                total_category_revenue = category_revenue.sum()

                if total_category_revenue > 0:

                    category_share = (
                        top_category_revenue
                        / total_category_revenue
                    ) * 100

                    insights.append(
                        f"📈 {top_category} contributes "
                        f"{category_share:.2f}% of total "
                        f"category revenue."
                    )

                # ------------------------------------------
                # TOP 3 CATEGORIES
                # ------------------------------------------

                top_categories = category_revenue.head(3)

                if len(top_categories) >= 2:

                    top_category_text = ", ".join(
                        [
                            f"{name} ({value:,.2f})"
                            for name, value
                            in top_categories.items()
                        ]
                    )

                    insights.append(
                        f"📊 Top categories by revenue: "
                        f"{top_category_text}."
                    )

    # ======================================================
    # GENERAL NUMERIC ANALYSIS
    # ======================================================

    for column in numeric_columns:

        # Skip columns already analyzed
        if column in ["Quantity", "Price"]:
            continue

        numeric_data = pd.to_numeric(
            df[column],
            errors="coerce"
        ).dropna()

        if numeric_data.empty:
            continue

        column_mean = numeric_data.mean()
        column_max = numeric_data.max()
        column_min = numeric_data.min()

        insights.append(
            f"📌 {column}: average "
            f"{column_mean:,.2f}, "
            f"maximum {column_max:,.2f}, "
            f"minimum {column_min:,.2f}."
        )

    # ======================================================
    # RECOMMENDATION
    # ======================================================

    if "Product" in df.columns and "Category" in df.columns:

        insights.append(
            "💡 Recommendation: Focus on the best-selling "
            "products and highest-revenue categories to "
            "identify opportunities for growth."
        )

    elif numeric_columns:

        insights.append(
            "💡 Recommendation: Review the key numeric "
            "metrics and dataset-quality indicators to "
            "identify opportunities for improvement."
        )

    else:

        insights.append(
            "💡 Recommendation: Explore the categorical "
            "patterns and data-quality indicators for "
            "further analysis."
        )

    # ======================================================
    # FINAL SAFETY CHECK
    # ======================================================

    if not isinstance(insights, list):
        return ["⚠️ Unable to generate dataset insights."]

    return insights