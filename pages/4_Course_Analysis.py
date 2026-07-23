import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils import charts

st.set_page_config(page_title="Course Analysis - EduPro", page_icon="🎓", layout="wide")
st.title("🎓 Course Analysis")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

st.plotly_chart(charts.category_popularity_bar(filtered), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.course_type_pie(filtered), use_container_width=True)
with col2:
    st.plotly_chart(charts.course_level_bar(filtered), use_container_width=True)

st.divider()
st.subheader("Enrollment Treemap")
st.plotly_chart(charts.category_treemap(filtered), use_container_width=True)

st.subheader("Category → Level Breakdown")
st.plotly_chart(charts.category_level_sunburst(filtered), use_container_width=True)
