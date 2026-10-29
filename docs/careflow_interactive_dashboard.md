\# Day 17: Interactive CareFlow Dashboard



\## Objective

The objective of Day 17 was to develop an interactive Streamlit dashboard to visualize CareFlow process mining results and understand patient workflow patterns.



\## Features

\- Displays key workflow performance metrics.

\- Visualizes activity frequency across patient cases.

\- Shows common patient journey pathways.

\- Displays transitions with higher average elapsed time.

\- Provides summary tables for workflow analysis.

\- Presents process insights in an easy-to-understand dashboard.



\## Dataset Overview

\- Total patient cases: 1,000

\- Total recorded events: 6,964

\- Unique activity types: 10

\- Recorded activity transitions: 5,964



\## Tools and Technologies

\- Python

\- Pandas

\- Streamlit

\- Matplotlib

\- CSV datasets



\## Methodology

The dashboard loads processed CareFlow summary CSV files and presents the results through KPI metrics, charts, and tables. It helps users explore activity frequency, patient pathway variations, and elapsed-time patterns.



\## Files Created

\- `src/careflow\_interactive\_dashboard.py`

\- `docs/careflow\_interactive\_dashboard.md`



\## Limitations

The dashboard depends on the processed CSV files being available. Elapsed time between recorded activities does not necessarily represent actual waiting time or confirm a process bottleneck.



\## Conclusion

The interactive dashboard provides a clear visual overview of CareFlow workflow analysis and makes process mining results easier to understand and explore.



