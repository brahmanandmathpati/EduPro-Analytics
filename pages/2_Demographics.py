import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils import charts

st.set_page_config(page_title="Demographics - EduPro", page_icon="👥", layout="wide")
st.title("👥 Learner Demographics")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

# Deduplicate to one row per learner for demographic-only charts
# (the master table has one row per ENROLLMENT, so a learner with 5
# courses would otherwise be counted 5 times in an age/gender chart)
learners_filtered = filtered.drop_duplicates(subset="UserID")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(charts.age_distribution_hist(learners_filtered), use_container_width=True)
with col2:
    st.plotly_chart(charts.gender_distribution_pie(learners_filtered), use_container_width=True)

st.plotly_chart(charts.age_group_bar(learners_filtered), use_container_width=True)

st.divider()
st.subheader("Age Distribution by Course Category")
st.caption("Boxplot uses enrollment-level data (not deduplicated) since it compares across categories.")
st.plotly_chart(charts.age_by_category_box(filtered), use_container_width=True)
