\# Day 8: Patient Waiting Time Analysis



\## Objective

Calculate elapsed time between consecutive recorded activities and summarize the time by activity transition.



\## Dataset

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Transitions analysed: 5,964



\## Methodology

1\. Loaded the supplied CareFlow dataset.

2\. Validated the required columns and checked for missing values.

3\. Converted timestamps to datetime format.

4\. Sorted activities by patient case and activity order.

5\. Calculated elapsed minutes between consecutive activity timestamps.

6\. Calculated average, median, and maximum elapsed time for each transition.



\## Key Findings

\- Lab Collection → Lab Result had the highest average elapsed time: 32.56 minutes.

\- Triage → Doctor Assessment had an average elapsed time of 30.74 minutes.

\- X-Ray → Radiology Result had an average elapsed time of 22.42 minutes.

\- Registration → Triage had an average elapsed time of 12.62 minutes.



\## Output Files

\- `src/patient\_waiting\_time\_analysis.py`

\- `data/processed/patient\_waiting\_time\_summary.csv`

\- `docs/patient\_waiting\_time\_analysis.md`



\## Conclusion

The analysis summarizes elapsed time between consecutive activities in the recorded patient pathways. Lab Collection → Lab Result showed the highest average elapsed interval among the analysed transitions.



\## Limitation

Elapsed time between recorded activities does not necessarily equal actual waiting time. The results alone do not establish operational bottlenecks or explain the causes of delays.

