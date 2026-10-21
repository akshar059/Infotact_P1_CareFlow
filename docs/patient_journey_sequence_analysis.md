\# Day 11: Patient Journey Sequence Analysis



\## Objective

Identify the different complete patient activity sequences in the CareFlow dataset and measure how frequently each sequence occurs.



\## Dataset Summary

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Unique complete journey sequences: 6



\## Methodology

1\. Loaded the CareFlow event dataset.

2\. Validated required columns and checked for missing values.

3\. Sorted activities by patient case and activity order.

4\. Combined each patient's activities into a complete sequence.

5\. Counted patients following each sequence.

6\. Calculated the percentage of patients for each sequence.

7\. Exported the results to a CSV file.



\## Key Findings

\- The most common sequence was Registration → Triage → Doctor Assessment → Discharge, followed by 267 patients (26.7%).

\- 216 patients (21.6%) followed the pathway involving X-Ray, Radiology Result, and Documentation Review.

\- 149 patients (14.9%) followed the pathway involving Lab Collection and Lab Result.

\- 146 patients (14.6%) followed a pathway with Triage and Doctor Reassessment repeated in the journey.

\- 133 patients (13.3%) followed a pathway involving both radiology and laboratory activities.

\- 89 patients (8.9%) followed a longer pathway involving radiology, reassessment, and laboratory activities.



\## Output Files

\- `src/patient\_journey\_sequence\_analysis.py`

\- `data/processed/patient\_journey\_sequence\_summary.csv`

\- `docs/patient\_journey\_sequence\_analysis.md`



\## Conclusion

The analysis identified six complete activity sequences in the supplied dataset. The most common sequence accounted for 26.7% of patient cases, while the remaining cases followed alternative pathways.



\## Limitation

These findings describe the supplied dataset. They do not independently explain why patients followed different pathways or establish clinical effectiveness or workflow efficiency.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

