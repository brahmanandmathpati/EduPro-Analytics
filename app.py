"""
app.py
------
Entry point for the Streamlit multi-page app. Streamlit auto-discovers
files in pages/ and adds them to the sidebar nav, so this file only
needs to render the Home page content.

Run with:  streamlit run app.py
"""

import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils.metrics import get_kpis

st.set_page_config(page_title="EduPro Analytics", page_icon="📊", layout="wide")

st.title("📊 EduPro Analytics Dashboard")
st.caption("Learner Demographics and Course Enrollment Behavior Analysis")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

st.markdown("""
Welcome! This dashboard explores **who** is learning on EduPro and **what**
they're enrolling in - age and gender patterns, category popularity, course
levels, and enrollment trends over time. Use the sidebar filters to slice
the data by any dimension.

*Note: Users data is real. Courses and Transactions data in this build are
synthetically generated for demonstration/learning purposes.*
""")

st.divider()

kpis = get_kpis(users, courses, filtered)

row1 = st.columns(4)
row1[0].metric("Total Learners", kpis["Total Learners"])
row1[1].metric("Total Courses", kpis["Total Courses"])
row1[2].metric("Total Enrollments", kpis["Total Enrollments"])
row1[3].metric("Avg Courses / Learner", kpis["Avg Courses Per Learner"])

row2 = st.columns(4)
row2[0].metric("Most Popular Category", kpis["Most Popular Category"])
row2[1].metric("Most Popular Course", kpis["Most Popular Course"])
row2[2].metric("Most Popular Level", kpis["Most Popular Level"])
row2[3].metric("Average Learner Age", kpis["Average Learner Age"])

row3 = st.columns(2)
row3[0].metric("Male %", f"{kpis['Male %']}%")
row3[1].metric("Female %", f"{kpis['Female %']}%")

st.divider()
st.subheader("Quick Insights")
st.markdown(f"""
- The platform's real learner base skews **young (ages 15-35)**.
- **{kpis['Most Popular Category']}** is the most popular course category.
- Learners take an average of **{kpis['Avg Courses Per Learner']}** courses each.
- Use the **Learner Demographics**, **Enrollment Analysis**, **Course Analysis**,
  and **Demographic Preferences** pages (left sidebar) to dig deeper into each area.
""")
