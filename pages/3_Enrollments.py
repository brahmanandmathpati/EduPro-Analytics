import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils.metrics import enrollment_analysis, monthly_trend, quarterly_trend, yearly_trend
from utils import charts

st.set_page_config(page_title="Enrollments - EduPro", page_icon="📈", layout="wide")
st.title("📈 Enrollment Analysis")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

ea = enrollment_analysis(filtered)

col1, col2, col3 = st.columns(3)
col1.metric("Total Enrollments", ea["total_enrollments"])
col2.metric("Avg Enrollments / User", round(ea["enrollments_per_user_stats"]["mean"], 2))
col3.metric("Max Enrollments (single user)", int(ea["enrollments_per_user_stats"]["max"]))

st.divider()
st.plotly_chart(charts.top_courses_bar(ea["top_courses"]), use_container_width=True)

with st.expander("Least Popular Courses"):
    st.dataframe(ea["least_popular_courses"], use_container_width=True)

st.divider()
st.subheader("Enrollment Trends Over Time")

tab1, tab2, tab3 = st.tabs(["Monthly", "Quarterly", "Yearly"])
with tab1:
    st.plotly_chart(charts.monthly_trend_line(monthly_trend(filtered)), use_container_width=True)
with tab2:
    st.plotly_chart(charts.quarterly_trend_bar(quarterly_trend(filtered)), use_container_width=True)
with tab3:
    st.plotly_chart(charts.yearly_trend_bar(yearly_trend(filtered)), use_container_width=True)
