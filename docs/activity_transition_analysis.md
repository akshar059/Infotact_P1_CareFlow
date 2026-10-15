\# Day 5: Activity Transition Analysis



\## Objective

Analyze consecutive patient activities to identify common transitions in the CareFlow clinical workflow.



\## Dataset

\- File: `data/raw/careflow\_events\_scaled.csv`

\- Total events: 6,964

\- Patient cases: 1,000



\## Analysis Performed

1\. Loaded the final CareFlow dataset.

2\. Checked the required columns.

3\. Sorted activities by patient case and activity order.

4\. Identified transitions between consecutive activities.

5\. Counted the frequency of each activity transition.

6\. Saved detailed transitions and summary results as CSV files.



\## Results

\- Total events analyzed: 6,964

\- Total transitions identified: 5,964

\- Unique transition types: 16



\### Most Common Transitions



| Activity Transition | Count |

|---|---:|

| Registration → Triage | 1,000 |

| Triage → Doctor Assessment | 1,000 |

| Doctor Assessment → X-Ray | 584 |

| X-Ray → Radiology Result | 584 |

| Lab Collection → Lab Result | 371 |



\## Initial Observations

Registration → Triage and Triage → Doctor Assessment are the most frequent transitions, each occurring 1,000 times.



X-Ray → Radiology Result occurs 584 times, while Lab Collection → Lab Result occurs 371 times.



These results describe the activity sequences recorded in the dataset. Further analysis is needed to determine why workflow variations occur and whether any transition represents a bottleneck.



\## Output Files

\- `src/activity\_transition\_analysis.py`

\- `data/processed/activity\_transition\_details.csv`

\- `data/processed/activity\_transition\_summary.csv`

\- `docs/activity\_transition\_analysis.md`



\## Conclusion

The activity transition analysis identifies common consecutive activities in the CareFlow dataset. These results can support further workflow discovery and process mining analysis.



\## Note

The analysis uses the team's supplied dataset. Results describe recorded transitions and do not independently establish operational causes or bottlenecks.

