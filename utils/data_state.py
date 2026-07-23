"""
data_state.py
--------------
Streamlit re-runs the whole script top-to-bottom on every interaction
(every filter click, every widget change). Without caching, that would
mean re-reading the Excel file and re-cleaning 9000+ rows on every
click - slow and wasteful. st.cache_data solves this: the expensive
pipeline only runs once per session (or when the file changes).
"""

import streamlit as st
from utils.preprocess import run_full_pipeline


@st.cache_data
def get_data(path: str = "data/EduPro.xlsx"):
    return run_full_pipeline(path)


def apply_sidebar_filters(master_df, users_df):
    """Renders sidebar filter widgets and returns the filtered master_df.

    Every page calls this so filters behave consistently everywhere.
    """
    st.sidebar.header("Filters")

    age_groups = st.sidebar.multiselect(
        "Age Group", options=sorted(master_df["AgeGroup"].dropna().unique().tolist()),
        default=None)
    genders = st.sidebar.multiselect(
        "Gender", options=sorted(master_df["Gender"].dropna().unique().tolist()),
        default=None)
    categories = st.sidebar.multiselect(
        "Course Category", options=sorted(master_df["CourseCategory"].dropna().unique().tolist()),
        default=None)
    course_types = st.sidebar.multiselect(
        "Course Type", options=sorted(master_df["CourseType"].dropna().unique().tolist()),
        default=None)
    levels = st.sidebar.multiselect(
        "Course Level", options=sorted(master_df["CourseLevel"].dropna().unique().tolist()),
        default=None)
    years = st.sidebar.multiselect(
        "Year", options=sorted(master_df["Year"].dropna().unique().tolist()),
        default=None)
    MONTH_ORDER = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    available_months = master_df["MonthName"].dropna().unique().tolist()
    month_options = [m for m in MONTH_ORDER if m in available_months]
    months = st.sidebar.multiselect("Month", options=month_options, default=None)

    filtered = master_df.copy()
    if age_groups:
        filtered = filtered[filtered["AgeGroup"].isin(age_groups)]
    if genders:
        filtered = filtered[filtered["Gender"].isin(genders)]
    if categories:
        filtered = filtered[filtered["CourseCategory"].isin(categories)]
    if course_types:
        filtered = filtered[filtered["CourseType"].isin(course_types)]
    if levels:
        filtered = filtered[filtered["CourseLevel"].isin(levels)]
    if years:
        filtered = filtered[filtered["Year"].isin(years)]
    if months:
        filtered = filtered[filtered["MonthName"].isin(months)]

    return filtered
