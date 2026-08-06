import pandas as pd


def load_csv(uploaded_file):
    """
    Load an uploaded CSV file into a Pandas DataFrame.

    Parameters:
        uploaded_file: Uploaded CSV file from Streamlit.

    Returns:
        pandas.DataFrame: Loaded dataset.
    """

    return pd.read_csv(uploaded_file)