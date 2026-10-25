\# Day 14: Workflow Performance Summary



\## Objective

Summarize patient workflow transition performance using transition frequency and elapsed-time statistics.



\## Dataset Summary

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Valid consecutive transitions analyzed: 5,964

\- Unique transition types: 16



\## Methodology

1\. Loaded the CareFlow event dataset.

2\. Validated required columns and checked for missing values.

3\. Converted timestamps to datetime format.

4\. Sorted activities by patient case and activity order.

5\. Identified consecutive activity transitions.

6\. Calculated elapsed time in minutes between consecutive activities.

7\. Summarized each transition using frequency, average elapsed time, median elapsed time, and maximum elapsed time.

8\. Ranked transitions by average elapsed time and frequency.

9\. Exported the summary to a CSV file.



\## Key Findings

\- Lab Collection → Lab Result had the highest average elapsed time of 32.56 minutes across 371 transitions.

\- Triage → Doctor Assessment occurred 1,000 times and had an average elapsed time of 30.74 minutes.

\- X-Ray → Radiology Result occurred 584 times and had an average elapsed time of 22.42 minutes.

\- Registration → Triage was one of the most frequent transitions, occurring 1,000 times.

\- The analysis identified 16 unique transition types.



\## Output Files

\- `src/workflow\_performance\_summary.py`

\- `data/processed/workflow\_performance\_summary.csv`

\- `docs/workflow\_performance\_summary.md`



\## Conclusion

The workflow performance summary provides a comparison of transition frequency and elapsed-time statistics. Lab Collection → Lab Result had the highest average elapsed interval, while Registration → Triage and Triage → Doctor Assessment were the most frequent transitions.



\## Limitations

Elapsed time measures the interval between recorded activities. It does not necessarily represent actual waiting time, prove a bottleneck, or establish its cause.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

