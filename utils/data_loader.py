import pandas as pd


def load_csv(uploaded_file):
    """
    Load an uploaded CSV file into a Pandas DataFrame.

    Parameters:
        uploaded_file: Uploaded CSV file from Streamlit.

    Returns:
        pandas.DataFrame: Loaded dataset.

    Raises:
        ValueError: If the CSV file cannot be loaded or is empty.
    """

    if uploaded_file is None:
        raise ValueError("No file was uploaded.")

    try:
        df = pd.read_csv(uploaded_file)

    except UnicodeDecodeError:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="latin1")
        except Exception as error:
            raise ValueError(
                "The CSV file could not be decoded. "
                "Please check the file encoding."
            ) from error

    except pd.errors.EmptyDataError as error:
        raise ValueError(
            "The uploaded CSV file is empty."
        ) from error

    except pd.errors.ParserError as error:
        raise ValueError(
            "The CSV file could not be parsed. "
            "Please make sure it is a valid CSV file."
        ) from error

    except Exception as error:
        raise ValueError(
            "An unexpected error occurred while loading the CSV file."
        ) from error

    if df.empty:
        raise ValueError(
            "The uploaded CSV file contains no data."
        )

    return df