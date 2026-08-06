import pandas as pd


def generate_insights(df):
    """
    Generate basic AI-style insights for the uploaded dataset.
    """

    insights = []

    # Dataset size
    insights.append(
        f"📊 Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
    )

    # Missing values
    missing = int(df.isnull().sum().sum())

    if missing == 0:
        insights.append("✅ No missing values found.")
    else:
        insights.append(f"⚠️ Dataset contains {missing} missing values.")

    # Duplicates
    duplicates = int(df.duplicated().sum())

    if duplicates == 0:
        insights.append("✅ No duplicate rows detected.")
    else:
        insights.append(f"⚠️ {duplicates} duplicate rows found.")

    # Numeric columns
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        insights.append(
            "🔢 Numeric Columns: " + ", ".join(numeric_columns)
        )

    # Categorical columns
    categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

    if categorical_columns:
        insights.append(
            "📝 Categorical Columns: " + ", ".join(categorical_columns)
        )

    # Recommendation
    insights.append(
        "💡 Recommendation: Use Bar/Pie charts for categorical columns and trend charts for numeric columns."
    )

    return insights