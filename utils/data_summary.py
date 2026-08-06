import pandas as pd


def get_dataset_info(df):
    """
    Generate summary information for each column in the dataset.

    Parameters:
        df (pandas.DataFrame): Input dataset.

    Returns:
        pandas.DataFrame: Column names, data types, and missing values.
    """

    dataset_info = pd.DataFrame(
        {
            "Column Name": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
        }
    )

    return dataset_info