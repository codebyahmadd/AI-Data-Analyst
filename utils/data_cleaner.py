import pandas as pd


def clean_data(df):
    """
    Perform basic data cleaning on the dataset.

    Operations:
        - Remove duplicate rows.
        - Replace missing values with "N/A".

    Parameters:
        df (pandas.DataFrame): Input dataset.

    Returns:
        pandas.DataFrame: Cleaned dataset.
    """

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Replace missing values
    cleaned_df = cleaned_df.fillna("N/A")

    return cleaned_df