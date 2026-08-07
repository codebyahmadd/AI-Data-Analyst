import pandas as pd


def generate_report(df, insights):
    """
    Generate a structured analysis report.
    """

    report = []

    # -----------------------------
    # Report Header
    # -----------------------------
    report.append("AI DATA ANALYST - ANALYSIS REPORT")
    report.append("=" * 50)
    report.append("")

    # -----------------------------
    # Dataset Summary
    # -----------------------------
    report.append("DATASET SUMMARY")
    report.append("-" * 50)

    report.append(f"Rows: {df.shape[0]:,}")
    report.append(f"Columns: {df.shape[1]:,}")

    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    report.append(f"Missing Values: {missing_values:,}")
    report.append(f"Duplicate Rows: {duplicate_rows:,}")
    report.append("")

    # -----------------------------
    # Column Information
    # -----------------------------
    report.append("COLUMN INFORMATION")
    report.append("-" * 50)

    for column in df.columns:
        dtype = str(df[column].dtype)
        unique_values = df[column].nunique()

        report.append(
            f"{column} | Type: {dtype} | "
            f"Unique Values: {unique_values:,}"
        )

    report.append("")

    # -----------------------------
    # AI Insights
    # -----------------------------
    report.append("AI INSIGHTS")
    report.append("-" * 50)

    for insight in insights:
        report.append(insight)

    report.append("")

    # -----------------------------
    # Statistical Summary
    # -----------------------------
    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:

        report.append("STATISTICAL SUMMARY")
        report.append("-" * 50)

        summary = numeric_df.describe()

        report.append(
            summary.round(2).to_string()
        )

    return "\n".join(report)