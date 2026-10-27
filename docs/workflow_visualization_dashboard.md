\# Day 16: Patient Workflow Visualization Dashboard



\## Objective

Create visual charts to make CareFlow process mining results easier to understand and review.



\## Dataset Summary

\- Total patient cases analyzed: 1,000

\- Total recorded events: 6,964

\- Activity types: 10

\- Patient journey sequences: 6

\- Consecutive transitions analyzed: 5,964



\## Methodology

1\. Loaded the existing activity frequency summary.

2\. Loaded the patient journey sequence summary.

3\. Loaded the workflow performance summary.

4\. Validated the required input files and columns.

5\. Generated charts using Pandas and Matplotlib.

6\. Saved the chart images in the `docs` directory.

7\. Exported pathway labels and their corresponding sequences to a CSV file.



\## Visualizations Created



\### 1. Activity Frequency Chart

File: `docs/activity\_frequency\_chart.png`



Displays the number of recorded events for each hospital activity, helping identify frequently recorded activities.



\### 2. Patient Pathway Chart

File: `docs/patient\_pathway\_chart.png`



Displays the six observed patient journey sequences and the number of cases following each pathway.



\### 3. Workflow Elapsed-Time Chart

File: `docs/workflow\_elapsed\_time\_chart.png`



Displays up to ten activity transitions with the highest average elapsed times, helping identify transitions that may require further investigation.



\## Output Files

\- `src/workflow\_visualization\_dashboard.py`

\- `docs/activity\_frequency\_chart.png`

\- `docs/patient\_pathway\_chart.png`

\- `docs/workflow\_elapsed\_time\_chart.png`

\- `data/processed/workflow\_visualization\_pathway\_details.csv`

\- `docs/workflow\_visualization\_dashboard.md`



\## Conclusion

The visualization script successfully generated three charts using the existing CareFlow analysis summaries. These charts make activity frequency, patient pathway variation, and elapsed-time patterns easier to review.



\## Limitations

The charts summarize the supplied dataset and do not establish clinical effectiveness or prove the cause of workflow delays. Elapsed time between recorded activities is not necessarily actual waiting time. Further investigation should consider timestamps, patient acuity, department workload, and operational context.



\## Data Note

The existing team dataset was used for analysis. The raw dataset was not included in the intended Git commit.



