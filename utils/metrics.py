"""
metrics.py
----------
Computes KPIs and EDA summary tables from the cleaned/merged data.
Kept separate from charts.py so the *numbers* (which might be shown
as text, in a table, or fed into a chart) aren't tangled up with
*how they're drawn*.
"""

import pandas as pd


def get_kpis(users_df: pd.DataFrame, courses_df: pd.DataFrame, master_df: pd.DataFrame) -> dict:
    """Compute the headline KPIs used on the dashboard's Home page."""
    total_learners = users_df["UserID"].nunique()
    total_courses = courses_df["CourseID"].nunique()
    total_transactions = len(master_df)
    total_enrollments = master_df["TransactionID"].nunique()

    avg_courses_per_learner = round(total_enrollments / total_learners, 2)

    most_popular_category = master_df["CourseCategory"].value_counts().idxmax()
    most_popular_course = master_df["CourseName"].value_counts().idxmax()
    most_popular_level = master_df["CourseLevel"].value_counts().idxmax()

    gender_counts = users_df["Gender"].value_counts(normalize=True) * 100
    male_pct = round(gender_counts.get("Male", 0), 1)
    female_pct = round(gender_counts.get("Female", 0), 1)

    avg_age = round(users_df["Age"].mean(), 1)

    return {
        "Total Learners": total_learners,
        "Total Courses": total_courses,
        "Total Transactions": total_transactions,
        "Total Enrollments": total_enrollments,
        "Avg Courses Per Learner": avg_courses_per_learner,
        "Most Popular Category": most_popular_category,
        "Most Popular Course": most_popular_course,
        "Most Popular Level": most_popular_level,
        "Male %": male_pct,
        "Female %": female_pct,
        "Average Learner Age": avg_age,
    }


def dataset_overview(df: pd.DataFrame) -> dict:
    """Basic dataset overview: shape, dtypes, missing values, summary stats."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "summary_stats": df.describe(include="all").to_dict(),
    }


def enrollment_analysis(master_df: pd.DataFrame) -> dict:
    """Enrollment counts, per-user stats, top/least popular courses."""
    enrollments_per_user = master_df.groupby("UserID").size()

    top_courses = (master_df["CourseName"].value_counts()
                   .head(10).reset_index())
    top_courses.columns = ["CourseName", "Enrollments"]

    least_courses = (master_df["CourseName"].value_counts()
                      .tail(10).reset_index())
    least_courses.columns = ["CourseName", "Enrollments"]

    return {
        "total_enrollments": len(master_df),
        "enrollments_per_user_stats": enrollments_per_user.describe().to_dict(),
        "top_courses": top_courses,
        "least_popular_courses": least_courses,
    }


def course_analysis(master_df: pd.DataFrame) -> dict:
    """Category / type / level distributions."""
    return {
        "category_distribution": master_df["CourseCategory"].value_counts().reset_index(
            name="Count").rename(columns={"index": "CourseCategory"}),
        "type_distribution": master_df["CourseType"].value_counts().reset_index(
            name="Count").rename(columns={"index": "CourseType"}),
        "level_distribution": master_df["CourseLevel"].value_counts().reset_index(
            name="Count").rename(columns={"index": "CourseLevel"}),
    }


def demographic_crosstabs(master_df: pd.DataFrame) -> dict:
    """Cross-tabulations for demographic insight charts (heatmaps etc.)."""
    return {
        "agegroup_vs_category": pd.crosstab(master_df["AgeGroup"], master_df["CourseCategory"]),
        "agegroup_vs_level": pd.crosstab(master_df["AgeGroup"], master_df["CourseLevel"]),
        "gender_vs_category": pd.crosstab(master_df["Gender"], master_df["CourseCategory"]),
        "gender_vs_level": pd.crosstab(master_df["Gender"], master_df["CourseLevel"]),
    }


def behavioral_analysis(master_df: pd.DataFrame) -> dict:
    """Average courses per learner, most active learners, concentration, repeats."""
    per_user = master_df.groupby("UserID").size().sort_values(ascending=False)

    most_active = per_user.head(10).reset_index()
    most_active.columns = ["UserID", "EnrollmentCount"]

    # Enrollment concentration: what % of enrollments come from the top 10%
    # of learners? (classic "power user" analysis)
    n_users = per_user.shape[0]
    top_10pct_n = max(1, int(n_users * 0.10))
    top_10pct_enrollments = per_user.head(top_10pct_n).sum()
    concentration_pct = round(top_10pct_enrollments / per_user.sum() * 100, 1)

    # Repeat enrollment: learners who enrolled in more than 1 course
    repeat_learners = (per_user > 1).sum()
    repeat_pct = round(repeat_learners / n_users * 100, 1)

    return {
        "average_courses_per_learner": round(per_user.mean(), 2),
        "most_active_learners": most_active,
        "top10pct_concentration_pct": concentration_pct,
        "repeat_learner_pct": repeat_pct,
    }


def monthly_trend(master_df: pd.DataFrame) -> pd.DataFrame:
    """Enrollment counts per Year-Month, sorted chronologically."""
    trend = (master_df.groupby(["Year", "Month", "MonthName"])
             .size().reset_index(name="Enrollments")
             .sort_values(["Year", "Month"]))
    return trend


def quarterly_trend(master_df: pd.DataFrame) -> pd.DataFrame:
    return (master_df.groupby(["Year", "Quarter"])
            .size().reset_index(name="Enrollments")
            .sort_values(["Year", "Quarter"]))


def yearly_trend(master_df: pd.DataFrame) -> pd.DataFrame:
    return master_df.groupby("Year").size().reset_index(name="Enrollments")
