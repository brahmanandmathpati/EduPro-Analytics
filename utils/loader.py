"""
loader.py
---------
Small, focused module: its only job is reading the Excel file into
three DataFrames. Keeping this separate from cleaning logic means
you can swap the data source (e.g. a database later) without
touching any cleaning code.
"""

import pandas as pd

DATA_PATH = "data/EduPro.xlsx"


def load_raw_data(path: str = DATA_PATH):
    """Load Users, Courses, and Transactions sheets from the Excel file.

    Returns
    -------
    tuple(pd.DataFrame, pd.DataFrame, pd.DataFrame)
        users_df, courses_df, transactions_df
    """
    users_df = pd.read_excel(path, sheet_name="Users")
    courses_df = pd.read_excel(path, sheet_name="Courses")
    transactions_df = pd.read_excel(path, sheet_name="Transactions")
    return users_df, courses_df, transactions_df
