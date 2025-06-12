"""Simple Data Loader for loading data from xlsx files."""

import pandas as pd
def load_data(file_path: str) -> pd.DataFrame:
    """"
    Load data from an Excel file.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the Excel file.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return pd.DataFrame()
    
