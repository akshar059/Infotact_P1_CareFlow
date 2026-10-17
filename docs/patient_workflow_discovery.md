\# Day 6: Patient Workflow Discovery



\## Objective

Discover the common clinical workflow and activity transitions in the CareFlow dataset using PM4Py.



\## Dataset

\- File: `data/raw/careflow\_events\_scaled.csv`

\- Total events: 6,964

\- Unique patient cases: 1,000



\## Analysis Performed

1\. Loaded and validated the dataset.

2\. Sorted activities by patient case and activity order.

3\. Prepared the event log using PM4Py.

4\. Discovered the Directly-Follows Graph (DFG).

5\. Identified start activities, end activities, and transition frequencies.

6\. Generated a workflow process map.



\## Results

\- Start activity: Registration (1,000 cases)

\- End activity: Discharge (1,000 cases)

\- Registration → Triage: 1,000 transitions

\- Triage → Doctor Assessment: 1,000 transitions

\- Doctor Assessment → X-Ray: 584 transitions

\- X-Ray → Radiology Result: 584 transitions

\- Lab Collection → Lab Result: 371 transitions



\## Output

\- `src/patient\_workflow\_discovery.py`

\- `docs/patient\_workflow\_map.svg`

\- `docs/patient\_workflow\_discovery.md`



\## Conclusion

The discovered workflow shows that all 1,000 patient cases begin with Registration and end with Discharge. The process map represents the recorded activity transitions and their frequencies.



\## Note

The analysis uses the team's supplied dataset. The results describe recorded workflow patterns and do not independently establish the causes of workflow variations or operational bottlenecks.

