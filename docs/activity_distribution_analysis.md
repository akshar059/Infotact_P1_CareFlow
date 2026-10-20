\# Day 10: Patient Activity Distribution Analysis



\## Objective

Analyze how patient activity is distributed across the CareFlow dataset by measuring event counts and the number and percentage of patients associated with each activity.



\## Dataset Summary

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Unique activity types: 10



\## Methodology

1\. Loaded the CareFlow event dataset.

2\. Validated required columns and checked for missing values.

3\. Counted recorded events for each activity.

4\. Counted unique patients associated with each activity.

5\. Calculated each activity's percentage of total events and total patients.

6\. Saved the results as a CSV file.



\## Key Findings

\- Triage had the highest event count, with 1,235 events across 1,000 patients.

\- Registration, Doctor Assessment, and Discharge each appeared for all 1,000 patients.

\- X-Ray, Radiology Result, and Documentation Review each appeared for 584 patients (58.4%).

\- Lab Collection and Lab Result each appeared for 371 patients (37.1%).

\- Doctor Reassessment appeared for 235 patients (23.5%).



\## Output Files

\- `src/activity\_distribution\_analysis.py`

\- `data/processed/activity\_distribution\_summary.csv`

\- `docs/activity\_distribution\_analysis.md`



\## Conclusion

The analysis describes how frequently each activity occurs and how many patients experience it. It shows that some activities occur in every patient case, while others occur only in a subset of cases.



\## Limitation

Activity distribution alone does not establish workflow efficiency, waiting times, or operational bottlenecks.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

