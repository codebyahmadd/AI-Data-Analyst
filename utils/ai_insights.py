import pandas as pd


def generate_insights(df):
    """
    Generate automatic insights for the uploaded dataset.
    """

    insights = []

    # -----------------------------
    # Dataset Size
    # -----------------------------
    rows = df.shape[0]
    columns = df.shape[1]

    insights.append(
        f"📊 Dataset contains {rows:,} rows and {columns} columns."
    )

    # -----------------------------
    # Missing Values
    # -----------------------------
    missing = int(df.isnull().sum().sum())

    if missing == 0:
        insights.append(
            "✅ No missing values found in the dataset."
        )
    else:
        insights.append(
            f"⚠️ Dataset contains {missing:,} missing values."
        )

    # -----------------------------
    # Duplicate Rows
    # -----------------------------
    duplicates = int(df.duplicated().sum())

    if duplicates == 0:
        insights.append(
            "✅ No duplicate rows detected."
        )
    else:
        insights.append(
            f"⚠️ {duplicates:,} duplicate rows found."
        )

    # -----------------------------
    # Numeric Columns
    # -----------------------------
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:
        insights.append(
            "🔢 Numeric Columns: "
            + ", ".join(numeric_columns)
        )

    # -----------------------------
    # Categorical Columns
    # -----------------------------
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical_columns:
        insights.append(
            "📝 Categorical Columns: "
            + ", ".join(categorical_columns)
        )

    # -----------------------------
    # Numeric Analysis
    # -----------------------------
    if numeric_columns:

        for column in numeric_columns[:5]:

            series = df[column].dropna()

            if series.empty:
                continue

            highest = series.max()
            lowest = series.min()

            insights.append(
                f"📈 {column}: minimum value is "
                f"{lowest:,.2f} and maximum value is "
                f"{highest:,.2f}."
            )

    # -----------------------------
    # Recommendation
    # -----------------------------
    if numeric_columns and categorical_columns:

        insights.append(
            "💡 Recommendation: Use categorical columns "
            "for comparison charts and numeric columns "
            "for statistical and trend analysis."
        )

    elif numeric_columns:

        insights.append(
            "💡 Recommendation: Focus on statistical "
            "analysis, distributions, and correlation "
            "between numeric columns."
        )

    elif categorical_columns:

        insights.append(
            "💡 Recommendation: Use Bar and Pie charts "
            "to explore categorical data."
        )

    else:

        insights.append(
            "💡 Recommendation: Review the dataset "
            "structure before performing further analysis."
        )

    return insights