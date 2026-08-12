def generate_report(df, insights=None):
    """
    Generate a structured text analysis report.
    """

    # =========================================================
    # SAFELY HANDLE INSIGHTS
    # =========================================================

    if insights is None:
        insights = []

    elif isinstance(insights, str):
        insights = [insights]

    elif not isinstance(insights, (list, tuple)):
        try:
            insights = list(insights)
        except TypeError:
            insights = [str(insights)]

    else:
        insights = list(insights)

    # Remove empty values
    insights = [
        str(insight).strip()
        for insight in insights
        if insight is not None and str(insight).strip()
    ]

    # =========================================================
    # REPORT
    # =========================================================

    report = []

    # =========================================================
    # HEADER
    # =========================================================

    report.append(
        "AI DATA ANALYST - ANALYSIS REPORT"
    )

    report.append("=" * 60)
    report.append("")

    # =========================================================
    # DATASET SUMMARY
    # =========================================================

    report.append("DATASET SUMMARY")
    report.append("-" * 60)

    rows = df.shape[0]
    columns = df.shape[1]

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    report.append(
        f"Rows: {rows:,}"
    )

    report.append(
        f"Columns: {columns:,}"
    )

    report.append(
        f"Missing Values: {missing_values:,}"
    )

    report.append(
        f"Duplicate Rows: {duplicate_rows:,}"
    )

    report.append("")

    # =========================================================
    # COLUMN INFORMATION
    # =========================================================

    report.append("COLUMN INFORMATION")
    report.append("-" * 60)

    for column in df.columns:

        dtype = str(
            df[column].dtype
        )

        unique_values = int(
            df[column].nunique(dropna=True)
        )

        report.append(
            f"{column} | "
            f"Type: {dtype} | "
            f"Unique Values: {unique_values:,}"
        )

    report.append("")

    # =========================================================
    # AI INSIGHTS
    # =========================================================

    report.append("AI INSIGHTS")
    report.append("-" * 60)

    if insights:

        for index, insight in enumerate(
            insights,
            start=1
        ):

            report.append(
                f"{index}. {insight}"
            )

    else:

        report.append(
            "No automatic insights were generated."
        )

    report.append("")

    # =========================================================
    # STATISTICAL SUMMARY
    # =========================================================

    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        report.append(
            "STATISTICAL SUMMARY"
        )

        report.append(
            "-" * 60
        )

        summary = numeric_df.describe()

        report.append(
            summary.round(2).to_string()
        )

        report.append("")

    # =========================================================
    # RETURN REPORT
    # =========================================================

    return "\n".join(report)