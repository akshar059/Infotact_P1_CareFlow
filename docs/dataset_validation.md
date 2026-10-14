\# Day 3: Dataset Validation



\## Objective

Validate the structure and basic data quality of the CareFlow sample event log before performing process mining analysis.



\## Dataset Details

\- \*\*File:\*\* `data/raw/sample\_event\_log.csv`

\- \*\*Total events:\*\* 16

\- \*\*Unique patient cases:\*\* 3

\- \*\*Required columns:\*\* `case\_id`, `activity`, `timestamp`



\## Validation Checks

1\. Checked whether all required columns are present.

2\. Checked missing values in required columns.

3\. Checked whether timestamps are valid.

4\. Checked whether events can be arranged chronologically within each patient case.

5\. Checked for exact duplicate rows.



\## Results

\- Required columns: PASS

\- Missing required values: 0

\- Invalid timestamps: 0

\- Chronological ordering: PASS

\- Exact duplicate rows: 0



\## Conclusion

The sample event log passed all implemented validation checks and is ready for the next stage of process mining analysis.



\*\*Note:\*\* This is a small synthetic sample dataset. These checks do not establish the accuracy or completeness of real hospital data.

