import streamlit as st
from utils.data_state import get_data, apply_sidebar_filters
from utils.metrics import get_kpis, behavioral_analysis
from utils import charts

st.set_page_config(page_title="Insights - EduPro", page_icon="💡", layout="wide")
st.title("💡 Insights & Recommendations")

data = get_data()
users, courses, master = data["users"], data["courses"], data["master"]
filtered = apply_sidebar_filters(master, users)

kpis = get_kpis(users, courses, filtered)
ba = behavioral_analysis(filtered)

st.subheader("Key Findings")
st.markdown(f"""
1. **Young learner base**: the real Users data spans only ages 15-35, with no
   learners recorded in the 36-45 or 46+ groups.
2. **{kpis['Most Popular Category']}** is the leading course category, and
   **{kpis['Most Popular Level']}**-level courses dominate enrollments overall.
3. **Repeat engagement is strong**: {ba['repeat_learner_pct']}% of learners
   enroll in more than one course.
4. **Enrollment is concentrated**: the top 10% most active learners account
   for {ba['top10pct_concentration_pct']}% of all enrollments - a classic
   "power user" pattern.
""")

st.divider()
st.subheader("Business Recommendations")
st.markdown("""
- Double down on **Beginner-level, high-volume categories** (e.g. Marketing,
  Programming) since they drive the bulk of enrollments.
- Design **retention campaigns** targeting the large repeat-learner segment
  to nudge them toward course bundles or subscriptions.
- Investigate why the 36+ age segment is absent - is it a marketing gap,
  a content-relevance gap, or simply outside the platform's target market?
""")

st.subheader("Government / Policy Recommendations")
st.markdown("""
- If this reflects a real regional pattern, it suggests **upskilling programs
  for learners under 35 are working**, but adults 36+ may need separate,
  targeted digital-literacy or reskilling initiatives.
- Encourage subsidized access to **higher-level (Advanced) courses**, since
  Beginner-level content currently dominates.
""")

st.subheader("Future Improvements")
st.markdown("""
- Replace synthetic Courses/Transactions data with real platform data once
  available.
- Add cohort/retention analysis (do learners come back month over month?).
- Add course completion and rating data, not just enrollment counts.
""")

st.divider()
st.plotly_chart(charts.enrollments_per_user_scatter(filtered, users), use_container_width=True)
