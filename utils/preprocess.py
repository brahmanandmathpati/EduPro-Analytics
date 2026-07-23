"""
preprocess.py
-------------
All data-cleaning and feature-engineering logic lives here, separate
from loading (loader.py) and charting (charts.py). This separation
is a common pattern: each file has ONE job, which makes debugging
much easier - if a number looks wrong, you know exactly which file
to check.
"""

import pandas as pd
import numpy as np

AGE_BINS = [0, 18, 26, 36, 46, 150]
AGE_LABELS = ["<18", "18-25", "26-35", "36-45", "46+"]


def clean_users(users_df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Users table.

    Steps:
      1. Drop exact duplicate rows.
      2. Drop rows missing UserID (can't be linked to anything).
      3. Standardize Gender text (e.g. 'male', 'M', 'Male' -> 'Male').
      4. Remove invalid ages (e.g. negative, or above 100).
      5. Fill any remaining missing Age with the median age.
    """
    df = users_df.copy()

    df = df.drop_duplicates()
    df = df.dropna(subset=["UserID"])

    # Standardize gender values: strip whitespace, fix casing
    df["Gender"] = df["Gender"].astype(str).str.strip().str.capitalize()
    df["Gender"] = df["Gender"].replace({"M": "Male", "F": "Female"})
    valid_genders = {"Male", "Female", "Other"}
    df.loc[~df["Gender"].isin(valid_genders), "Gender"] = "Other"

    # Age must be a sensible human age
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df.loc[(df["Age"] < 5) | (df["Age"] > 100), "Age"] = np.nan
    median_age = df["Age"].median()
    df["Age"] = df["Age"].fillna(median_age).astype(int)

    return df.reset_index(drop=True)


def clean_courses(courses_df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Courses table: drop duplicates/missing IDs, trim text."""
    df = courses_df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["CourseID"])

    for col in ["CourseName", "CourseCategory", "CourseType", "CourseLevel"]:
        df[col] = df[col].astype(str).str.strip()

    return df.reset_index(drop=True)


def clean_transactions(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Transactions table.

    Steps:
      1. Drop duplicates and rows missing key IDs.
      2. Convert TransactionDate to real datetime objects (this is
         essential - without it, we can't extract Year/Month/etc.
         or plot time trends correctly).
      3. Drop rows where the date failed to parse.
    """
    df = transactions_df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["UserID", "CourseID"])

    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors="coerce")
    df = df.dropna(subset=["TransactionDate"])

    return df.reset_index(drop=True)


def add_age_groups(users_df: pd.DataFrame) -> pd.DataFrame:
    """Bucket Age into groups: <18, 18-25, 26-35, 36-45, 46+."""
    df = users_df.copy()
    df["AgeGroup"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    return df


def add_date_parts(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """Extract Year, Month, Quarter, and Day Name from TransactionDate."""
    df = transactions_df.copy()
    df["Year"] = df["TransactionDate"].dt.year
    df["Month"] = df["TransactionDate"].dt.month
    df["MonthName"] = df["TransactionDate"].dt.strftime("%B")
    df["Quarter"] = df["TransactionDate"].dt.quarter
    df["DayName"] = df["TransactionDate"].dt.strftime("%A")
    return df


def build_master_table(users_df, courses_df, transactions_df) -> pd.DataFrame:
    """Merge Users -> Transactions -> Courses into one analysis-ready table.

    This is the table almost every chart and KPI will be built from.
    """
    users_clean = add_age_groups(clean_users(users_df))
    courses_clean = clean_courses(courses_df)
    transactions_clean = add_date_parts(clean_transactions(transactions_df))

    master = transactions_clean.merge(users_clean, on="UserID", how="left")
    master = master.merge(courses_clean, on="CourseID", how="left")

    return master


def run_full_pipeline(path: str = "data/EduPro.xlsx"):
    """Convenience function: load + clean + merge in one call."""
    from utils.loader import load_raw_data

    users_df, courses_df, transactions_df = load_raw_data(path)
    users_clean = add_age_groups(clean_users(users_df))
    courses_clean = clean_courses(courses_df)
    transactions_clean = add_date_parts(clean_transactions(transactions_df))
    master = build_master_table(users_df, courses_df, transactions_df)

    return {
        "users": users_clean,
        "courses": courses_clean,
        "transactions": transactions_clean,
        "master": master,
    }
