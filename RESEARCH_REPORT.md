# Learner Demographics and Course Enrollment Behavior Analysis on EduPro

**A Descriptive Analytics Research Report**

---

## Abstract

This report presents a descriptive analysis of learner demographics and
course enrollment behavior on the EduPro online learning platform. Using
3,000 real learner records combined with course and transaction data, the
analysis examines age and gender distribution, course category and level
popularity, enrollment concentration, and time-based enrollment trends.
Key findings show a young, evenly gender-split learner base (ages 15-35,
50.7% female / 49.3% male) with high repeat engagement (69.5% of learners
enroll in more than one course) and a moderate concentration effect, where
the top 10% of learners account for 28.5% of all enrollments. Marketing
and Programming are the leading course categories, and Beginner-level
content dominates enrollment volume.

*Note: Course and Transaction data used in this analysis are synthetically
generated (see Methodology) because the original dataset provided only
learner demographic records. Findings involving courses/enrollments should
be read as a demonstration of the analytical method, not as verified
real-world platform behavior, until real course/transaction data is
substituted.*

---

## Introduction

Online learning platforms generate large volumes of behavioral data, but
that data only becomes useful once it is cleaned, structured, and
explored. This project analyzes learner demographics (age, gender) against
course enrollment behavior (category, level, timing) to surface patterns
that could inform platform strategy — which content to expand, which
learner segments are underserved, and how engagement is distributed across
the user base.

## Problem Statement

EduPro (like many learning platforms) accumulates enrollment data without
a clear picture of *who* is enrolling in *what*, or *when*. Without this
visibility, content and marketing decisions are made on intuition rather
than evidence. This project addresses that gap through structured,
descriptive analysis — no predictive modeling is used, keeping the scope
focused on understanding the current state of the data.

## Objectives

1. Clean and merge the Users, Courses, and Transactions datasets into a
   single analysis-ready table.
2. Quantify learner demographics (age distribution, gender split, age
   groups).
3. Quantify enrollment behavior (top/least popular courses, category and
   level popularity, enrollment concentration).
4. Cross-tabulate demographics against course preferences (age group vs.
   category, gender vs. level, etc.).
5. Surface time-based enrollment trends (monthly, quarterly, yearly).
6. Translate findings into actionable business and policy recommendations.

## Dataset Description

| Sheet | Rows | Key Columns | Source |
|---|---|---|---|
| Users | 3,000 | UserID, UserName, Age, Gender, Email | Real |
| Courses | 40 | CourseID, CourseName, CourseCategory, CourseType, CourseLevel | Synthetic |
| Transactions | 9,164 | TransactionID, UserID, CourseID, TransactionDate | Synthetic |

Synthetic Courses/Transactions were generated with structure rather than
pure randomness: course popularity follows a power-law-like distribution
(a few courses dominate enrollment, most don't), enrollment counts per
learner follow a realistic long-tail (most learners take 1-4 courses, a
small "power user" segment takes many more), and category preference is
softly correlated with age band, mimicking plausible real-world patterns.

## Methodology

### Data Cleaning
- Removed duplicate rows and rows with missing primary keys.
- Standardized Gender values (whitespace/casing normalized; invalid
  values mapped to "Other").
- Removed implausible ages (<5 or >100) and imputed the remainder with
  the median age.
- Converted `TransactionDate` to proper datetime objects, dropping rows
  where parsing failed.
- Merged Users → Transactions → Courses on `UserID` and `CourseID` into
  one master table (9,164 rows, zero missing values after merge).

### Feature Engineering
- **Age Groups**: `<18`, `18-25`, `26-35`, `36-45`, `46+`
- **Date parts**: Year, Month, Month Name, Quarter, Day Name — extracted
  from `TransactionDate` to support all time-trend analysis.

### EDA & Visualization
Descriptive statistics and 17 Plotly visualizations (bar, pie/donut,
histogram, line, stacked/grouped bar, heatmap, treemap, sunburst, boxplot,
scatter) were produced across demographics, enrollment, course, and
cross-tabulated demographic-preference views. See the Streamlit dashboard
for the interactive versions of every chart referenced below.

## Insights

**Demographics**
- The real learner base spans ages **15-35 only** — no learners aged 36+
  appear in the dataset. Age groups: `<18` = 433, `18-25` = 1,121,
  `26-35` = 1,446, `36-45` = 0, `46+` = 0.
- Gender split is nearly even: **50.7% Female, 49.3% Male**.
- Average learner age: **25.0 years**.

**Enrollment Behavior**
- Total enrollments: **9,164** across **3,000 learners** (avg. **3.05**
  courses/learner).
- Top course: *SEO Fundamentals* (968 enrollments), followed by *Adobe
  Illustrator Essentials* (671) and *Object Oriented Programming* (623).
- Least popular: *Figma Masterclass* (37 enrollments) and *Python for Data
  Science* (39).
- **69.5%** of learners enrolled in more than one course (strong repeat
  engagement).
- The top 10% most active learners account for **28.5%** of all
  enrollments — a moderate concentration effect, not an extreme one.

**Course Preferences**
- **Marketing** is the leading category (2,567 enrollments), followed by
  Programming (1,273) and Personal Development (1,257). Cloud Computing
  is least popular (599).
- **Beginner**-level courses dominate (5,244 enrollments, 57% of total),
  followed by Intermediate (3,282) and Advanced (638).
- **Paid** courses outnumber Free ones roughly 2.4:1 (6,440 vs. 2,724).

**Time Trend**
- Enrollment grew from **3,492** (2024) to **5,672** (2025) — a ~62%
  year-over-year increase, consistent with the mild upward trend built
  into the synthetic transaction dates.

## Business Recommendations

- Prioritize content investment in **Marketing and Programming**, the two
  highest-enrollment categories.
- Since Beginner-level content drives the majority of volume, consider
  building clearer **Beginner → Intermediate → Advanced** learning paths
  to convert existing engagement into higher-value course completions.
- Target the **repeat-learner segment (69.5%)** with bundle or
  subscription offers, since they are already demonstrating multi-course
  intent.
- Investigate low-performing courses (*Figma Masterclass*, *Python for
  Data Science*) for pricing, marketing, or content-quality issues before
  assuming low intrinsic demand.

## Government / Policy Recommendations

*(Speculative — contingent on this pattern reflecting a real regional
population once real data is used.)*

- The complete absence of learners aged 36+ may indicate a **digital
  upskilling gap** for older workers; targeted digital-literacy or
  reskilling outreach could help close it.
- Public subsidy or grant programs could focus on **increasing Advanced-
  level course access**, since Advanced content is currently the smallest
  segment (638 enrollments, ~7% of total) despite likely economic value.

## Conclusion

This analysis demonstrates a complete descriptive-analytics pipeline —
cleaning, merging, feature engineering, EDA, and visualization — applied
to learner demographic and enrollment data. Even with synthetic
course/transaction data, the pipeline surfaces coherent, actionable
patterns: a young and gender-balanced learner base, strong repeat
engagement, a moderate concentration of activity among top learners, and
clear category/level preferences. The modular codebase (`loader.py`,
`preprocess.py`, `metrics.py`, `charts.py`) is structured so that swapping
in real Courses/Transactions data requires no changes to the analysis
logic itself.

## Future Scope

- Replace synthetic Courses/Transactions data with real platform data.
- Add cohort and retention analysis (do learners return month-over-month?).
- Incorporate course completion rates and learner ratings, not just
  enrollment counts, to distinguish engagement from genuine value delivery.
- Extend the age range check once real data with a broader age spread is
  available, to confirm whether the 36+ gap is a data artifact or a real
  platform pattern.
