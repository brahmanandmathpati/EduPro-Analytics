"""
charts.py
---------
Every chart function takes clean data in and returns a Plotly Figure.
Keeping charts as pure functions (data in -> figure out) means the
Streamlit pages can just call them and st.plotly_chart(fig) - no
plotting logic lives inside the dashboard pages themselves.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

TEMPLATE = "plotly_dark"
COLOR_SEQ = px.colors.qualitative.Set2


def age_distribution_hist(users_df: pd.DataFrame):
    fig = px.histogram(users_df, x="Age", nbins=20, template=TEMPLATE,
                        color_discrete_sequence=COLOR_SEQ,
                        title="Age Distribution of Learners")
    fig.update_layout(bargap=0.05)
    return fig


def gender_distribution_pie(users_df: pd.DataFrame):
    counts = users_df["Gender"].value_counts().reset_index()
    counts.columns = ["Gender", "Count"]
    fig = px.pie(counts, names="Gender", values="Count", hole=0.45,
                 template=TEMPLATE, color_discrete_sequence=COLOR_SEQ,
                 title="Gender Distribution (Donut)")
    return fig


def age_group_bar(users_df: pd.DataFrame):
    counts = users_df["AgeGroup"].value_counts().sort_index().reset_index()
    counts.columns = ["AgeGroup", "Count"]
    fig = px.bar(counts, x="AgeGroup", y="Count", template=TEMPLATE,
                 color="AgeGroup", color_discrete_sequence=COLOR_SEQ,
                 title="Age Group Distribution")
    return fig


def category_popularity_bar(master_df: pd.DataFrame):
    counts = master_df["CourseCategory"].value_counts().reset_index()
    counts.columns = ["CourseCategory", "Enrollments"]
    fig = px.bar(counts, x="Enrollments", y="CourseCategory", orientation="h",
                 template=TEMPLATE, color="Enrollments",
                 color_continuous_scale="Teal",
                 title="Course Category Popularity")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def course_type_pie(master_df: pd.DataFrame):
    counts = master_df["CourseType"].value_counts().reset_index()
    counts.columns = ["CourseType", "Count"]
    fig = px.pie(counts, names="CourseType", values="Count", template=TEMPLATE,
                 color_discrete_sequence=COLOR_SEQ, title="Course Type (Free vs Paid)")
    return fig


def course_level_bar(master_df: pd.DataFrame):
    counts = master_df["CourseLevel"].value_counts().reset_index()
    counts.columns = ["CourseLevel", "Count"]
    fig = px.bar(counts, x="CourseLevel", y="Count", template=TEMPLATE,
                 color="CourseLevel", color_discrete_sequence=COLOR_SEQ,
                 title="Course Level Distribution")
    return fig


def monthly_trend_line(trend_df: pd.DataFrame):
    df = trend_df.copy()
    df["Period"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
    fig = px.line(df, x="Period", y="Enrollments", markers=True,
                  template=TEMPLATE, color_discrete_sequence=COLOR_SEQ,
                  title="Monthly Enrollment Trend")
    fig.update_xaxes(tickangle=45)
    return fig


def quarterly_trend_bar(trend_df: pd.DataFrame):
    df = trend_df.copy()
    df["Period"] = df["Year"].astype(str) + "-Q" + df["Quarter"].astype(str)
    fig = px.bar(df, x="Period", y="Enrollments", template=TEMPLATE,
                 color_discrete_sequence=COLOR_SEQ, title="Quarterly Enrollment Trend")
    return fig


def yearly_trend_bar(trend_df: pd.DataFrame):
    fig = px.bar(trend_df, x="Year", y="Enrollments", template=TEMPLATE,
                 color_discrete_sequence=COLOR_SEQ, title="Yearly Enrollment Trend")
    return fig


def agegroup_category_heatmap(crosstab_df: pd.DataFrame):
    fig = px.imshow(crosstab_df, template=TEMPLATE, color_continuous_scale="Teal",
                     aspect="auto", title="Age Group vs Course Category")
    return fig


def gender_level_grouped_bar(crosstab_df: pd.DataFrame):
    df = crosstab_df.reset_index().melt(id_vars="Gender", var_name="CourseLevel", value_name="Count")
    fig = px.bar(df, x="CourseLevel", y="Count", color="Gender", barmode="group",
                 template=TEMPLATE, color_discrete_sequence=COLOR_SEQ,
                 title="Gender vs Course Level")
    return fig


def top_courses_bar(top_courses_df: pd.DataFrame):
    fig = px.bar(top_courses_df, x="Enrollments", y="CourseName", orientation="h",
                 template=TEMPLATE, color="Enrollments", color_continuous_scale="Teal",
                 title="Top 10 Courses by Enrollment")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def most_active_learners_bar(active_df: pd.DataFrame):
    fig = px.bar(active_df, x="EnrollmentCount", y="UserID", orientation="h",
                 template=TEMPLATE, color="EnrollmentCount", color_continuous_scale="Teal",
                 title="Top 10 Most Active Learners")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig


def category_treemap(master_df: pd.DataFrame):
    counts = master_df.groupby(["CourseCategory", "CourseName"]).size().reset_index(name="Enrollments")
    fig = px.treemap(counts, path=["CourseCategory", "CourseName"], values="Enrollments",
                      template=TEMPLATE, color="Enrollments", color_continuous_scale="Teal",
                      title="Enrollment Treemap by Category / Course")
    return fig


def category_level_sunburst(master_df: pd.DataFrame):
    counts = master_df.groupby(["CourseCategory", "CourseLevel"]).size().reset_index(name="Enrollments")
    fig = px.sunburst(counts, path=["CourseCategory", "CourseLevel"], values="Enrollments",
                       template=TEMPLATE, color="Enrollments", color_continuous_scale="Teal",
                       title="Category -> Level Sunburst")
    return fig


def age_by_category_box(master_df: pd.DataFrame):
    fig = px.box(master_df, x="CourseCategory", y="Age", template=TEMPLATE,
                 color="CourseCategory", color_discrete_sequence=COLOR_SEQ,
                 title="Age Distribution by Course Category (Boxplot)")
    fig.update_xaxes(tickangle=30)
    fig.update_layout(showlegend=False)
    return fig


def enrollments_per_user_scatter(master_df: pd.DataFrame, users_df: pd.DataFrame):
    per_user = master_df.groupby("UserID").size().reset_index(name="EnrollmentCount")
    merged = per_user.merge(users_df[["UserID", "Age"]], on="UserID", how="left")
    fig = px.scatter(merged, x="Age", y="EnrollmentCount", template=TEMPLATE,
                      color_discrete_sequence=COLOR_SEQ, opacity=0.5,
                      title="Age vs Number of Enrollments")
    return fig
