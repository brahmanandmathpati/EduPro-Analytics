# 📊 EduPro Analytics — Learner Demographics & Course Enrollment Behavior

A descriptive analytics project exploring **who** learns on the EduPro
platform and **what** they enroll in — age & gender patterns, category
popularity, course levels, and enrollment trends over time.

> **Data note:** The `Users` sheet is real platform data (3,000 learners).
> `Courses` and `Transactions` are **synthetically generated** for this
> build, since the original dataset only included Users. See
> `generate_synthetic_data.py` for the generation logic. Replace
> `data/EduPro.xlsx` with real Courses/Transactions data to make every
> insight fully authentic.

---

## Features

- End-to-end pipeline: load → clean → merge → analyze → visualize
- 11 KPIs (total learners, courses, enrollments, avg courses/learner,
  most popular category/course/level, gender split, average age)
- 17 interactive Plotly charts (bar, pie/donut, histogram, line, heatmap,
  treemap, sunburst, boxplot, scatter)
- 6-page Streamlit dashboard with sidebar filters (age group, gender,
  category, type, level, year, month)
- Modular codebase (`utils/loader.py`, `preprocess.py`, `metrics.py`,
  `charts.py`) — each file has a single responsibility

## Dataset

| Sheet | Columns | Source |
|---|---|---|
| Users | UserID, UserName, Age, Gender, Email | Real |
| Courses | CourseID, CourseName, CourseCategory, CourseType, CourseLevel | Synthetic |
| Transactions | TransactionID, UserID, CourseID, TransactionDate | Synthetic |

## Installation

```bash
git clone <your-repo-url>
cd EduPro-Analytics
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Requirements

See `requirements.txt`: streamlit, pandas, numpy, plotly, matplotlib,
seaborn, openpyxl.

## How to Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).
Regenerate the dataset any time with:

```bash
python generate_synthetic_data.py
```

## Folder Structure

```
EduPro-Analytics/
├── app.py                      # Home page (entry point)
├── generate_synthetic_data.py  # Builds Courses + Transactions
├── requirements.txt
├── README.md
├── data/
│   └── EduPro.xlsx             # 3-sheet workbook: Users, Courses, Transactions
├── pages/
│   ├── 2_Demographics.py
│   ├── 3_Enrollments.py
│   ├── 4_Course_Analysis.py
│   ├── 5_Preferences.py
│   └── 6_Insights.py
├── utils/
│   ├── loader.py       # Reads the Excel sheets
│   ├── preprocess.py   # Cleaning, age groups, date parts, merge
│   ├── metrics.py       # KPIs and EDA summary tables
│   ├── charts.py        # Plotly figure builders
│   └── data_state.py    # Caching + sidebar filter logic
└── assets/
```

## KPIs Tracked

Total Learners · Total Courses · Total Transactions · Total Enrollments ·
Avg Courses per Learner · Most Popular Category/Course/Level · Male % ·
Female % · Average Learner Age

## Dashboard Pages

1. **Home** — overview + KPIs + quick insights
2. **Learner Demographics** — age, gender, age group, age-by-category boxplot
3. **Enrollment Analysis** — top/least popular courses, monthly/quarterly/yearly trends
4. **Course Analysis** — category, type, level distributions, treemap, sunburst
5. **Demographic Preferences** — age-group × category heatmap, gender × level
6. **Insights & Recommendations** — key findings, business & policy recommendations

## Future Improvements

- Swap in real Courses/Transactions data
- Add cohort/retention analysis
- Add course completion & rating data
- Add authentication for a real production deployment

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app**, select the repo, branch, and `app.py` as the entry file.
4. Deploy — Streamlit Cloud installs `requirements.txt` automatically.
