import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils.metrics import demographic_crosstabs
from utils import charts

st.set_page_config(page_title="Preferences - EduPro", page_icon="🧭", layout="wide")
st.title("🧭 Demographic Preferences")
st.caption("How different age groups and genders engage with course categories and levels.")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

ct = demographic_crosstabs(filtered)

st.subheader("Age Group vs Course Category")
st.plotly_chart(charts.agegroup_category_heatmap(ct["agegroup_vs_category"]), use_container_width=True)

st.subheader("Gender vs Course Level")
st.plotly_chart(charts.gender_level_grouped_bar(ct["gender_vs_level"]), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Age Group vs Course Level")
    st.dataframe(ct["agegroup_vs_level"], use_container_width=True)
with col2:
    st.subheader("Gender vs Course Category")
    st.dataframe(ct["gender_vs_category"], use_container_width=True)
