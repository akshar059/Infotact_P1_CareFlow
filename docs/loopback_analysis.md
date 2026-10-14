\# Day 4: Patient Workflow Loopback Analysis



\## Objective

Analyze loopback-marked events and repeated activities in the CareFlow dataset to understand patient workflow patterns.



\## Dataset

\- File: `data/raw/careflow\_events\_scaled.csv`

\- Total events: 6,964

\- Unique patient cases: 1,000



\## Analysis Performed

1\. Identified events marked as loopbacks.

2\. Counted loopback events by activity.

3\. Identified patient cases containing at least one loopback.

4\. Summarized activities marked as repeated.



\## Results

\- Loopback-marked events: 705

\- Cases with loopbacks: 235

\- Doctor Reassessment loopback events: 235

\- Documentation Review loopback events: 235

\- Triage loopback events: 235

\- Repeated Triage events: 235



\## Initial Observation

The dataset contains a consistent pattern of loopback-marked events across Doctor Reassessment, Documentation Review, and Triage. Triage is also marked as a repeated activity in 235 events.



These results identify workflow patterns for further investigation. They do not, by themselves, establish the cause of the loopbacks or prove that these activities are operational bottlenecks.



\## Output Files

\- `data/processed/loopback\_events.csv`

\- `data/processed/loopback\_activity\_summary.csv`

\- `data/processed/loopback\_case\_summary.csv`

\- `data/processed/repeat\_activity\_summary.csv`



\## Note

The analysis uses the team's supplied CareFlow dataset. Dataset flags were analyzed as provided; their underlying business rules should be confirmed before drawing operational conclusions.

