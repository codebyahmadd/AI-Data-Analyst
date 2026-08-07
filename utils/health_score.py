def calculate_health_score(df):
    """
    Calculate an overall dataset health score from 0 to 100.
    """

    score = 100

    # -----------------------------
    # Missing Values Penalty
    # -----------------------------
    total_cells = df.shape[0] * df.shape[1]

    if total_cells > 0:
        missing_cells = int(df.isnull().sum().sum())
        missing_percentage = (missing_cells / total_cells) * 100

        score -= min(missing_percentage, 30)
    else:
        missing_percentage = 0

    # -----------------------------
    # Duplicate Rows Penalty
    # -----------------------------
    duplicate_count = int(df.duplicated().sum())

    if df.shape[0] > 0:
        duplicate_percentage = (
            duplicate_count / df.shape[0]
        ) * 100

        score -= min(duplicate_percentage, 20)
    else:
        duplicate_percentage = 0

    # -----------------------------
    # Final Score
    # -----------------------------
    score = max(0, round(score))

    return {
        "score": score,
        "missing_percentage": round(missing_percentage, 2),
        "duplicate_percentage": round(duplicate_percentage, 2),
        "duplicate_count": duplicate_count,
    }


def get_health_status(score):
    """
    Return a health status based on the dataset score.
    """

    if score >= 90:
        return "Excellent", "🟢"

    if score >= 75:
        return "Good", "🟡"

    if score >= 50:
        return "Needs Improvement", "🟠"

    return "Poor", "🔴"