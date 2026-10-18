\# Day 7: Patient Pathway Variation Analysis



\## Objective

Identify different patient activity sequences and find the most common pathways in the CareFlow dataset.



\## Dataset

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Unique patient pathways: 6



\## Methodology

1\. Loaded the supplied CareFlow event dataset.

2\. Checked the required columns.

3\. Sorted activities by patient case and activity order.

4\. Created an ordered activity sequence for each case.

5\. Counted the cases following each unique pathway.

6\. Calculated the percentage of cases for each pathway.



\## Key Findings

\- The most common pathway was Registration → Triage → Doctor Assessment → Discharge, followed by 267 cases (26.7%).

\- 216 cases (21.6%) followed the X-Ray, Radiology Result, and Documentation Review pathway before discharge.

\- 149 cases (14.9%) followed the Lab Collection and Lab Result pathway before discharge.

\- Six unique complete activity sequences were identified in the supplied dataset.



\## Output

\- `src/pathway\_variation\_analysis.py`

\- `data/processed/pathway\_variation\_summary.csv`

\- `docs/pathway\_variation\_analysis.md`



\## Conclusion

The analysis identified six distinct recorded patient pathways. The most common sequence accounted for 26.7% of cases. These results describe patterns in the supplied dataset and do not independently explain why pathway variations occur.



\## Note

The analysis uses the team's supplied dataset. The dataset was not added to Git staging as part of this task.

