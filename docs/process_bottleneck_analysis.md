\# Day 13: Process Bottleneck Candidate Analysis



\## Objective

Analyze elapsed time between consecutive patient activities to identify workflow transitions that may require further investigation for potential delays.



\## Dataset Summary

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Valid consecutive transitions: 5,964

\- Unique transition types: 16



\## Methodology

1\. Loaded the CareFlow event dataset.

2\. Validated required columns and checked for missing values.

3\. Converted event timestamps into datetime format.

4\. Sorted events by patient case and activity order.

5\. Calculated elapsed minutes between consecutive activities.

6\. Grouped transitions and calculated transition count, average elapsed time, median elapsed time, and maximum elapsed time.

7\. Ranked transitions by average elapsed time and exported the results to CSV.



\## Key Findings

\- Lab Collection → Lab Result had the highest average elapsed time of 32.56 minutes across 371 transitions.

\- Triage → Doctor Assessment had an average elapsed time of 30.74 minutes across 1,000 transitions.

\- X-Ray → Radiology Result had an average elapsed time of 22.42 minutes across 584 transitions.

\- Documentation Review → Discharge had an average elapsed time of 15.50 minutes across 216 transitions.

\- Doctor Reassessment → Discharge had an average elapsed time of 15.37 minutes across 146 transitions.



\## Output Files

\- `src/process\_bottleneck\_analysis.py`

\- `data/processed/process\_bottleneck\_summary.csv`

\- `docs/process\_bottleneck\_analysis.md`



\## Conclusion

The analysis ranked 16 patient workflow transitions by average elapsed time. Lab Collection → Lab Result and Triage → Doctor Assessment showed the highest average elapsed intervals in the supplied dataset. These transitions may be prioritized for further investigation.



\## Limitations

Elapsed time between recorded activities does not necessarily equal actual waiting time. High elapsed time alone does not confirm a process bottleneck, its cause, or a negative clinical outcome.



\## Data Note

The team's raw dataset was used for analysis and was not included in the Git commit.

