import pandas as pd


def clean_data(df):
    """
    Clean the dataset by removing duplicates
    and filling missing values.
    """

    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Fill missing values
    cleaned_df = cleaned_df.fillna("N/A")

    return cleaned_df