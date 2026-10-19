\# Day 9: Patient Activity Frequency Analysis



\## Objective

Measure how frequently each activity appears in the CareFlow dataset and identify repeated activity occurrences.



\## Dataset

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Unique activity types: 10



\## Methodology

1\. Loaded the supplied CareFlow dataset.

2\. Validated the required columns and checked for missing values.

3\. Sorted events by patient case and activity order.

4\. Counted events for each activity.

5\. Calculated the number and percentage of cases containing each activity.

6\. Counted occurrences beyond the first occurrence of the same activity within a case.



\## Key Findings

\- Triage was the most frequently recorded activity, with 1,235 events.

\- Registration, Doctor Assessment, and Discharge each appeared 1,000 times.

\- X-Ray, Radiology Result, and Documentation Review each appeared 584 times.

\- Lab Collection and Lab Result each appeared 371 times.

\- Doctor Reassessment appeared 235 times.

\- Triage had 235 repeated occurrences beyond the first occurrence within each case.



\## Output Files

\- `src/activity\_frequency\_analysis.py`

\- `data/processed/activity\_frequency\_summary.csv`

\- `docs/activity\_frequency\_analysis.md`



\## Conclusion

The analysis summarizes the frequency of all 10 activity types and highlights repeated Triage occurrences. These findings describe the supplied dataset and do not independently explain the reasons for repeated activities.



\## Limitation

Activity frequency alone does not establish workflow efficiency, delays, or operational bottlenecks.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

