\# Day 12: Patient Journey Transition Analysis



\## Objective

Analyze consecutive activities in patient journeys to identify the most frequent transitions between activities.



\## Dataset Summary

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Total consecutive transitions: 5,964

\- Unique transition types: 16



\## Methodology

1\. Loaded the CareFlow event dataset.

2\. Validated the required columns and checked for missing values.

3\. Sorted activities by patient case and activity order.

4\. Identified the next activity for each recorded event within the same patient case.

5\. Counted each consecutive activity transition.

6\. Calculated the percentage of total transitions.

7\. Exported the transition summary to a CSV file.



\## Key Findings

\- Registration → Triage occurred 1,000 times (16.77% of transitions).

\- Triage → Doctor Assessment occurred 1,000 times (16.77%).

\- Doctor Assessment → X-Ray occurred 584 times (9.79%).

\- X-Ray → Radiology Result occurred 584 times (9.79%).

\- Lab Collection → Lab Result occurred 371 times (6.22%).

\- Lab Result → Discharge occurred 371 times (6.22%).

\- Radiology Result → Documentation Review occurred 349 times (5.85%).

\- Radiology Result → Triage occurred 235 times (3.94%).



\## Output Files

\- `src/patient\_journey\_transition\_analysis.py`

\- `data/processed/patient\_journey\_transition\_summary.csv`

\- `docs/patient\_journey\_transition\_analysis.md`



\## Conclusion

The analysis identified 16 types of consecutive activity transitions. Registration → Triage and Triage → Doctor Assessment were the most frequent transitions in the supplied dataset.



\## Limitation

Transition frequency alone does not establish delays, workflow bottlenecks, or clinical outcomes.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

