import pandas as pd
import re

print("AI_CHAT_V2_LOADED")


# ==========================================================
# SALES CALCULATION
# ==========================================================

def calculate_sales(df):
    """
    Calculate sales using Quantity × Price.
    """

    if "Quantity" in df.columns and "Price" in df.columns:

        quantity = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        )

        price = pd.to_numeric(
            df["Price"],
            errors="coerce"
        )

        return quantity * price

    return None


# ==========================================================
# FIND NUMERIC COLUMN
# ==========================================================

def find_numeric_column(df, question):
    """
    Find the numeric column mentioned in the question.
    """

    question = question.lower().strip()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Exact column matching
    for column in numeric_columns:

        column_name = str(column).lower().strip()

        if column_name in question:
            return column

    # Keyword matching
    keyword_mapping = {
        "quantity": ["quantity", "qty", "units"],
        "price": ["price", "cost"],
        "orderid": ["orderid", "order id", "order"],
    }

    for column in numeric_columns:

        column_name = str(column).lower()

        for key, keywords in keyword_mapping.items():

            if key in column_name:

                if any(
                    word in question
                    for word in keywords
                ):
                    return column

    return None


# ==========================================================
# FIND PRODUCT FROM QUESTION
# ==========================================================

def find_product(df, question):
    """
    Find a product name mentioned in the question.
    """

    if "Product" not in df.columns:
        return None

    products = (
        df["Product"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    # Longest names first
    products = sorted(
        products,
        key=len,
        reverse=True
    )

    for product in products:

        if product.lower() in question.lower():
            return product

    return None


# ==========================================================
# FIND CATEGORY FROM QUESTION
# ==========================================================

def find_category(df, question):
    """
    Find a category mentioned in the question.
    """

    if "Category" not in df.columns:
        return None

    categories = (
        df["Category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    categories = sorted(
        categories,
        key=len,
        reverse=True
    )

    for category in categories:

        if category.lower() in question.lower():
            return category

    return None


# ==========================================================
# TOP N
# ==========================================================

def get_top_n(question, default=3):
    """
    Extract Top N from a question.
    """

    match = re.search(
        r"\btop\s+(\d+)\b",
        question.lower()
    )

    if match:
        return int(match.group(1))

    return default


# ==========================================================
# MAIN QUESTION ANSWER FUNCTION
# ==========================================================

def answer_question(df, question):
    """
    Answer questions about the uploaded dataset.
    """

    question = str(question).lower().strip()

    print("QUESTION:", question)

    # ======================================================
    # DATASET SIZE
    # ======================================================

    if (
        "how many rows" in question
        or "number of rows" in question
        or "how many records" in question
        or "number of records" in question
        or question == "rows"
    ):

        return (
            f"📊 The dataset contains "
            f"{df.shape[0]:,} rows."
        )

    if (
        "how many columns" in question
        or "number of columns" in question
        or question == "columns"
    ):

        return (
            f"📊 The dataset contains "
            f"{df.shape[1]:,} columns."
        )

    # ======================================================
    # MISSING VALUES
    # ======================================================

    if (
        "missing" in question
        or "null" in question
        or "empty values" in question
    ):

        missing = int(
            df.isnull().sum().sum()
        )

        if missing == 0:

            return (
                "✅ The dataset has "
                "no missing values."
            )

        return (
            f"⚠️ The dataset contains "
            f"{missing:,} missing values."
        )

    # ======================================================
    # DUPLICATES
    # ======================================================

    if (
        "duplicate" in question
        or "duplicates" in question
        or "repeated rows" in question
    ):

        duplicates = int(
            df.duplicated().sum()
        )

        if duplicates == 0:

            return (
                "✅ The dataset contains "
                "no duplicate rows."
            )

        return (
            f"⚠️ The dataset contains "
            f"{duplicates:,} duplicate rows."
        )

    # ======================================================
    # COLUMN NAMES
    # ======================================================

    if (
        "column names" in question
        or "what columns" in question
        or "list columns" in question
        or "columns are there" in question
    ):

        columns = ", ".join(
            map(str, df.columns)
        )

        return (
            f"📋 The dataset columns are: "
            f"{columns}"
        )

    # ======================================================
    # NUMERIC COLUMNS
    # ======================================================

    if (
        "numeric columns" in question
        or "numerical columns" in question
    ):

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if not numeric_columns:

            return (
                "There are no numeric "
                "columns in the dataset."
            )

        return (
            "🔢 Numeric columns: "
            + ", ".join(
                map(str, numeric_columns)
            )
        )

    # ======================================================
    # CATEGORICAL COLUMNS
    # ======================================================

    if (
        "categorical columns" in question
        or "category columns" in question
    ):

        categorical_columns = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        if not categorical_columns:

            return (
                "There are no categorical "
                "columns in the dataset."
            )

        return (
            "📝 Categorical columns: "
            + ", ".join(
                map(str, categorical_columns)
            )
        )

    # ======================================================
    # PRODUCTS LIST
    # ======================================================

    if (
        "list products" in question
        or "product names" in question
        or "what products" in question
        or question == "products"
    ):

        if "Product" in df.columns:

            products = (
                df["Product"]
                .dropna()
                .unique()
                .tolist()
            )

            return (
                "🛍️ Products in the dataset: "
                + ", ".join(
                    map(str, products)
                )
            )

    # ======================================================
    # CATEGORIES LIST
    # ======================================================

    if (
        "list categories" in question
        or "category names" in question
        or "what categories" in question
        or question == "categories"
    ):

        if "Category" in df.columns:

            categories = (
                df["Category"]
                .dropna()
                .unique()
                .tolist()
            )

            return (
                "🏷️ Categories in the dataset: "
                + ", ".join(
                    map(str, categories)
                )
            )

    # ======================================================
    # SALES CALCULATION
    # ======================================================

    sales = calculate_sales(df)

    # ======================================================
    # PRODUCT-SPECIFIC QUESTIONS
    # ======================================================

    product = find_product(
        df,
        question
    )

    if (
        product is not None
        and sales is not None
    ):

        product_mask = (
            df["Product"]
            .astype(str)
            .str.lower()
            == product.lower()
        )

        product_sales = sales[product_mask]

        product_quantity = pd.to_numeric(
            df.loc[product_mask, "Quantity"],
            errors="coerce"
        ).sum()

        # --------------------------------------------------
        # PRODUCT REVENUE
        # --------------------------------------------------

        if (
            "revenue" in question
            or "sales" in question
            or "made" in question
            or "generated" in question
            or "earned" in question
        ):

            value = product_sales.sum()

            return (
                f"💰 {product} generated "
                f"{value:,.2f} in sales."
            )

        # --------------------------------------------------
        # PRODUCT QUANTITY
        # --------------------------------------------------

        if (
            "how many" in question
            or "how much" in question
            or "units" in question
            or "quantity" in question
            or "sold" in question
        ):

            return (
                f"📦 {product} has "
                f"{product_quantity:,.0f} units sold."
            )

    # ======================================================
    # CATEGORY-SPECIFIC QUESTIONS
    # ======================================================

    category = find_category(
        df,
        question
    )

    if (
        category is not None
        and sales is not None
    ):

        category_mask = (
            df["Category"]
            .astype(str)
            .str.lower()
            == category.lower()
        )

        category_sales = sales[category_mask]

        category_quantity = pd.to_numeric(
            df.loc[category_mask, "Quantity"],
            errors="coerce"
        ).sum()

        # --------------------------------------------------
        # CATEGORY REVENUE
        # --------------------------------------------------

        if (
            "revenue" in question
            or "sales" in question
            or "generated" in question
            or "made" in question
        ):

            value = category_sales.sum()

            return (
                f"💰 {category} generated "
                f"{value:,.2f} in sales."
            )

        # --------------------------------------------------
        # CATEGORY QUANTITY
        # --------------------------------------------------

        if (
            "how many" in question
            or "units" in question
            or "quantity" in question
            or "sold" in question
        ):

            return (
                f"📦 {category} has "
                f"{category_quantity:,.0f} units sold."
            )

    # ======================================================
    # BEST-SELLING PRODUCT
    # ======================================================

    if (
        "best selling product" in question
        or "best-selling product" in question
        or "top selling product" in question
        or "top-selling product" in question
        or "most sold product" in question
        or "which product sold the most" in question
        or "what product sold the most" in question
        or "product sold the most" in question
        or "most popular product" in question
    ):

        if (
            "Product" in df.columns
            and "Quantity" in df.columns
        ):

            product_data = df.copy()

            product_data["Quantity"] = pd.to_numeric(
                product_data["Quantity"],
                errors="coerce"
            )

            product_quantity = (
                product_data
                .groupby("Product")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not product_quantity.empty:

                product = product_quantity.index[0]
                quantity = product_quantity.iloc[0]

                return (
                    f"🏆 The best-selling product is "
                    f"{product}, with "
                    f"{quantity:,.0f} units sold."
                )

    # ======================================================
    # BEST-SELLING CATEGORY
    # ======================================================

    if (
        "best selling category" in question
        or "best-selling category" in question
        or "top selling category" in question
        or "top-selling category" in question
        or "most sold category" in question
        or "which category sold the most" in question
        or "what category sold the most" in question
        or "category sold the most" in question
        or "most popular category" in question
    ):

        if (
            "Category" in df.columns
            and "Quantity" in df.columns
        ):

            category_data = df.copy()

            category_data["Quantity"] = pd.to_numeric(
                category_data["Quantity"],
                errors="coerce"
            )

            category_quantity = (
                category_data
                .groupby("Category")["Quantity"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_quantity.empty:

                category = category_quantity.index[0]
                quantity = category_quantity.iloc[0]

                return (
                    f"🏆 The best-selling category is "
                    f"{category}, with "
                    f"{quantity:,.0f} units sold."
                )

    # ======================================================
    # TOP N PRODUCTS BY REVENUE
    # ======================================================

    if (
        sales is not None
        and "Product" in df.columns
        and (
            "top " in question
            or "top products" in question
            or "highest revenue products" in question
            or "best products by revenue" in question
        )
    ):

        n = get_top_n(question, 3)

        revenue_data = df.copy()
        revenue_data["CalculatedSales"] = sales

        product_revenue = (
            revenue_data
            .groupby("Product")["CalculatedSales"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
        )

        if not product_revenue.empty:

            result = "🏆 Top products by revenue:\n\n"

            for index, (name, value) in enumerate(
                product_revenue.items(),
                start=1
            ):

                result += (
                    f"{index}. {name} — "
                    f"{value:,.2f}\n"
                )

            return result.rstrip()

    # ======================================================
    # TOP N PRODUCTS BY QUANTITY
    # ======================================================

    if (
        "Product" in df.columns
        and "Quantity" in df.columns
        and (
            "top " in question
            or "highest quantity products" in question
            or "most sold products" in question
        )
    ):

        n = get_top_n(question, 3)

        quantity_data = df.copy()

        quantity_data["Quantity"] = pd.to_numeric(
            quantity_data["Quantity"],
            errors="coerce"
        )

        product_quantity = (
            quantity_data
            .groupby("Product")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
        )

        if not product_quantity.empty:

            result = "📦 Top products by units sold:\n\n"

            for index, (name, value) in enumerate(
                product_quantity.items(),
                start=1
            ):

                result += (
                    f"{index}. {name} — "
                    f"{value:,.0f} units\n"
                )

            return result.rstrip()

    # ======================================================
    # TOP PRODUCT BY REVENUE
    # ======================================================

    if (
        "highest revenue" in question
        or "highest revenue product" in question
        or "product with highest revenue" in question
        or "product with the highest revenue" in question
        or "what product has the highest revenue" in question
        or "which product has the highest revenue" in question
        or "top product by revenue" in question
        or "best product by revenue" in question
        or "what product made the most money" in question
        or "which product made the most money" in question
        or "product generated the most revenue" in question
        or "which product generated the most revenue" in question
        or "what product generated the most revenue" in question
        or "highest sales product" in question
        or "product with highest sales" in question
        or "product with the highest sales" in question
        or "what product has the highest sales" in question
        or "which product has the highest sales" in question
    ):

        if (
            sales is not None
            and "Product" in df.columns
        ):

            revenue_data = df.copy()

            revenue_data["CalculatedSales"] = sales

            product_revenue = (
                revenue_data
                .groupby("Product")["CalculatedSales"]
                .sum()
                .sort_values(ascending=False)
            )

            if not product_revenue.empty:

                product = product_revenue.index[0]
                revenue = product_revenue.iloc[0]

                return (
                    f"💰 The product with the "
                    f"highest revenue is "
                    f"{product}, generating "
                    f"{revenue:,.2f} in sales."
                )

    # ======================================================
    # TOP CATEGORY BY REVENUE
    # ======================================================

    if (
        "highest revenue category" in question
        or "category with highest revenue" in question
        or "category with the highest revenue" in question
        or "which category generated the most revenue" in question
        or "what category generated the most revenue" in question
        or "which category made the most money" in question
        or "what category made the most money" in question
        or "top category by revenue" in question
        or "best category by revenue" in question
    ):

        if (
            sales is not None
            and "Category" in df.columns
        ):

            revenue_data = df.copy()

            revenue_data["CalculatedSales"] = sales

            category_revenue = (
                revenue_data
                .groupby("Category")["CalculatedSales"]
                .sum()
                .sort_values(ascending=False)
            )

            if not category_revenue.empty:

                category = category_revenue.index[0]
                revenue = category_revenue.iloc[0]

                return (
                    f"💰 The highest-revenue category is "
                    f"{category}, generating "
                    f"{revenue:,.2f} in sales."
                )

    # ======================================================
    # TOTAL SALES
    # ======================================================

    if sales is not None:

        if (
            "total sales" in question
            or "total sale" in question
            or "total revenue" in question
            or "sum of sales" in question
            or "sum sales" in question
            or "how much did we sell" in question
            or "how much revenue" in question
        ):

            value = sales.sum()

            return (
                f"💰 The total sales are "
                f"{value:,.2f}."
            )

        # ==================================================
        # AVERAGE SALES
        # ==================================================

        if (
            "average sales" in question
            or "average sale" in question
            or "mean sales" in question
            or "mean sale" in question
            or "average revenue" in question
        ):

            value = sales.mean()

            return (
                f"📈 The average sales are "
                f"{value:,.2f}."
            )

        # ==================================================
        # HIGHEST SALES
        # ==================================================

        if (
            "highest sales" in question
            or "highest sale" in question
            or "maximum sales" in question
            or "maximum sale" in question
            or "max sales" in question
            or "max sale" in question
        ):

            value = sales.max()

            return (
                f"🔝 The highest sales are "
                f"{value:,.2f}."
            )

        # ==================================================
        # LOWEST SALES
        # ==================================================

        if (
            "lowest sales" in question
            or "lowest sale" in question
            or "minimum sales" in question
            or "minimum sale" in question
            or "min sales" in question
            or "min sale" in question
        ):

            value = sales.min()

            return (
                f"🔻 The lowest sales are "
                f"{value:,.2f}."
            )

    # ======================================================
    # OTHER NUMERIC COLUMN QUESTIONS
    # ======================================================

    numeric_column = find_numeric_column(
        df,
        question
    )

    if numeric_column is not None:

        if (
            "average" in question
            or "mean" in question
        ):

            value = df[numeric_column].mean()

            return (
                f"📈 The average "
                f"{numeric_column} is "
                f"{value:,.2f}."
            )

        if (
            "highest" in question
            or "maximum" in question
            or "max" in question
        ):

            value = df[numeric_column].max()

            return (
                f"🔝 The highest "
                f"{numeric_column} is "
                f"{value:,.2f}."
            )

        if (
            "lowest" in question
            or "minimum" in question
            or "min" in question
        ):

            value = df[numeric_column].min()

            return (
                f"🔻 The lowest "
                f"{numeric_column} is "
                f"{value:,.2f}."
            )

        if (
            "total" in question
            or "sum" in question
        ):

            value = df[numeric_column].sum()

            return (
                f"💰 The total "
                f"{numeric_column} is "
                f"{value:,.2f}."
            )

    # ======================================================
    # FALLBACK
    # ======================================================

    return (
        "🤔 I couldn't understand that question yet.\n\n"
        "Try asking:\n"
        "• How many rows are in the dataset?\n"
        "• Are there any missing values?\n"
        "• Are there any duplicate rows?\n"
        "• What are the column names?\n"
        "• What are the numeric columns?\n"
        "• What is the average sales?\n"
        "• What is the highest sales?\n"
        "• What is the lowest sales?\n"
        "• What is the total sales?\n"
        "• What is the best selling product?\n"
        "• What is the best selling category?\n"
        "• Which product generated the most revenue?\n"
        "• How much revenue did Phone generate?\n"
        "• How many Pens were sold?\n"
        "• Which category generated the most revenue?\n"
        "• Show me the top 3 products by revenue.\n"
        "• What is the average price?\n"
        "• What is the highest quantity?"
    )