import pandas as pd


def get_dataset_statistics(df):
    """
    Returns descriptive statistics for all numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return None

    stats = numeric_df.describe().transpose()

    stats = stats.round(2)

    return stats


def get_column_summary(df):
    """
    Returns summary of dataset columns.
    """

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(include=["object", "category"]).columns
    )

    datetime_columns = len(
        df.select_dtypes(include=["datetime"]).columns
    )

    return {
        "Numeric": numeric_columns,
        "Categorical": categorical_columns,
        "Datetime": datetime_columns
    }


def get_missing_report(df):
    """
    Returns missing values report.
    """

    report = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    return report