import pandas as pd


def clean_data(df):
    """
    Clean and standardize the uploaded dataset.

    Cleaning operations:
    - Remove completely empty rows and columns
    - Remove duplicate rows
    - Clean column names
    - Handle missing values based on column type
    - Convert numeric-looking columns to numeric values

    Parameters:
        df (pandas.DataFrame): Input dataset.

    Returns:
        pandas.DataFrame: Cleaned dataset.
    """

    if df is None:
        raise ValueError("No dataset was provided.")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    cleaned_df = df.copy()

    # --------------------------------------------------
    # Remove completely empty rows and columns
    # --------------------------------------------------

    cleaned_df = cleaned_df.dropna(
        axis=0,
        how="all"
    )

    cleaned_df = cleaned_df.dropna(
        axis=1,
        how="all"
    )

    # --------------------------------------------------
    # Clean column names
    # --------------------------------------------------

    cleaned_df.columns = (
        cleaned_df.columns
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )

    # --------------------------------------------------
    # Remove duplicate rows
    # --------------------------------------------------

    cleaned_df = cleaned_df.drop_duplicates()

    # --------------------------------------------------
    # Convert numeric-looking columns
    # --------------------------------------------------

    for column in cleaned_df.columns:

        if cleaned_df[column].dtype == "object":

            converted = pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )

            non_null_original = cleaned_df[column].notna().sum()

            non_null_converted = converted.notna().sum()

            if (
                non_null_original > 0
                and non_null_converted / non_null_original >= 0.8
            ):
                cleaned_df[column] = converted

    # --------------------------------------------------
    # Fill missing values
    # --------------------------------------------------

    for column in cleaned_df.columns:

        if pd.api.types.is_numeric_dtype(
            cleaned_df[column]
        ):

            median_value = cleaned_df[column].median()

            if pd.notna(median_value):
                cleaned_df[column] = (
                    cleaned_df[column].fillna(median_value)
                )

        else:

            mode = cleaned_df[column].mode()

            if not mode.empty:

                cleaned_df[column] = (
                    cleaned_df[column].fillna(mode.iloc[0])
                )

            else:

                cleaned_df[column] = (
                    cleaned_df[column].fillna("N/A")
                )

    # --------------------------------------------------
    # Reset index
    # --------------------------------------------------

    cleaned_df = cleaned_df.reset_index(
        drop=True
    )

    return cleaned_df