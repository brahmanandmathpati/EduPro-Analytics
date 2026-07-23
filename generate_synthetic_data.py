"""
generate_synthetic_data.py
---------------------------
Creates SYNTHETIC Courses and Transactions data to accompany the real
Users.csv data, so the full EduPro analytics pipeline can run end-to-end.

IMPORTANT: This data is artificially generated for learning/practice
purposes. It is NOT real enrollment data. Disclose this if the project
is shared as a portfolio piece.

Design choices (so the synthetic data has believable patterns instead
of pure randomness):
  - Course popularity follows a power-law-ish distribution (a few
    courses are very popular, most are not) - this mimics real
    enrollment platforms.
  - Younger learners are biased slightly toward "Beginner" level and
    categories like "Web Development" / "Programming".
  - Older learners are biased slightly toward "Data Science" /
    "Business" and "Advanced" level.
  - Transaction dates span 2 years with a mild upward monthly trend
    (platform growing over time) plus weekday seasonality.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)  # seed = reproducible results

# ------------------------------------------------------------------
# 1. COURSES TABLE
# ------------------------------------------------------------------
categories = ["Web Development", "Data Science", "Business", "Design",
              "Marketing", "Programming", "Cloud Computing", "Personal Development"]
course_types = ["Free", "Paid"]
course_levels = ["Beginner", "Intermediate", "Advanced"]

course_name_bank = {
    "Web Development": ["HTML & CSS Basics", "JavaScript Essentials", "React for Beginners",
                         "Full Stack Web Dev", "Responsive Design Masterclass"],
    "Data Science": ["Python for Data Science", "Statistics Fundamentals", "Data Visualization with Plotly",
                      "SQL for Analysts", "Data Science Capstone"],
    "Business": ["Business Analytics 101", "Financial Modeling", "Project Management Basics",
                 "Entrepreneurship Essentials", "Strategic Management"],
    "Design": ["UI/UX Design Fundamentals", "Graphic Design Basics", "Figma Masterclass",
               "Design Thinking Workshop", "Adobe Illustrator Essentials"],
    "Marketing": ["Digital Marketing 101", "SEO Fundamentals", "Social Media Marketing",
                  "Content Marketing Strategy", "Email Marketing Mastery"],
    "Programming": ["Python Programming Basics", "Java for Beginners", "C++ Fundamentals",
                     "Data Structures & Algorithms", "Object Oriented Programming"],
    "Cloud Computing": ["AWS Fundamentals", "Azure for Beginners", "Cloud Architecture Basics",
                         "DevOps Essentials", "Docker & Kubernetes Intro"],
    "Personal Development": ["Time Management Mastery", "Public Speaking Basics",
                              "Critical Thinking Skills", "Leadership Essentials", "Productivity Hacks"],
}

courses = []
course_id = 1
for cat, names in course_name_bank.items():
    for name in names:
        courses.append({
            "CourseID": f"C{course_id:05d}",
            "CourseName": name,
            "CourseCategory": cat,
            "CourseType": rng.choice(course_types, p=[0.35, 0.65]),
            "CourseLevel": rng.choice(course_levels, p=[0.5, 0.35, 0.15]),
        })
        course_id += 1

courses_df = pd.DataFrame(courses)
n_courses = len(courses_df)
print(f"Generated {n_courses} courses")

# Give each course a "popularity weight" (power law: few very popular courses)
popularity_weights = rng.pareto(a=2.0, size=n_courses) + 0.1
popularity_weights = popularity_weights / popularity_weights.sum()

# ------------------------------------------------------------------
# 2. LOAD USERS (real data)
# ------------------------------------------------------------------
users_df = pd.read_csv("/home/claude/EduPro-Analytics/data/Users_raw.csv")
n_users = len(users_df)
print(f"Loaded {n_users} users")

# ------------------------------------------------------------------
# 3. TRANSACTIONS TABLE
# ------------------------------------------------------------------
# Each user enrolls in a random number of courses (most enroll in 1-4,
# a smaller "power user" tail enrolls in many more)
enrollments_per_user = rng.choice(
    [1, 2, 3, 4, 5, 6, 7, 8, 10, 15],
    size=n_users,
    p=[0.30, 0.25, 0.15, 0.10, 0.07, 0.05, 0.03, 0.02, 0.02, 0.01]
)

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

# Mild growth trend: more transactions in later months
day_weights = np.linspace(0.5, 1.5, date_range_days + 1)
day_weights = day_weights / day_weights.sum()

transactions = []
txn_id = 1
for _, user in users_df.iterrows():
    n_enroll = enrollments_per_user[user.name]

    # Age-based category bias (soft nudge, not a hard rule)
    age = user["Age"]
    weights = popularity_weights.copy()
    if age < 26:
        boost_cats = ["Web Development", "Programming", "Design"]
    elif age < 36:
        boost_cats = ["Data Science", "Cloud Computing", "Marketing"]
    else:
        boost_cats = ["Business", "Personal Development", "Data Science"]
    boost_mask = courses_df["CourseCategory"].isin(boost_cats).values
    weights = weights * (1 + boost_mask * 0.6)
    weights = weights / weights.sum()

    chosen_course_idx = rng.choice(n_courses, size=min(n_enroll, n_courses),
                                    replace=False, p=weights)
    chosen_days = rng.choice(date_range_days + 1, size=len(chosen_course_idx), p=day_weights)

    for c_idx, day_offset in zip(chosen_course_idx, chosen_days):
        txn_date = start_date + timedelta(days=int(day_offset))
        transactions.append({
            "TransactionID": f"T{txn_id:06d}",
            "UserID": user["UserID"],
            "CourseID": courses_df.iloc[c_idx]["CourseID"],
            "TransactionDate": txn_date.strftime("%Y-%m-%d"),
        })
        txn_id += 1

transactions_df = pd.DataFrame(transactions)
print(f"Generated {len(transactions_df)} transactions")

# ------------------------------------------------------------------
# 4. SAVE TO A MULTI-SHEET EXCEL FILE (matches the original spec)
# ------------------------------------------------------------------
out_path = "/home/claude/EduPro-Analytics/data/EduPro.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    users_df.to_excel(writer, sheet_name="Users", index=False)
    courses_df.to_excel(writer, sheet_name="Courses", index=False)
    transactions_df.to_excel(writer, sheet_name="Transactions", index=False)

print(f"\nSaved: {out_path}")
print(f"  Users:        {len(users_df)} rows")
print(f"  Courses:      {len(courses_df)} rows")
print(f"  Transactions: {len(transactions_df)} rows")
