# CareFlow – Emergency Department Clinical Process Mining & Analytics

## 🚑 Project Overview
CareFlow is an end-to-end data analytics and process mining framework designed to evaluate patient throughput, identify clinical bottlenecks, isolate duration outliers, and optimize resource allocation within hospital Emergency Departments (ED).

---

## 🔑 Key Clinical Findings & Performance Metrics
- **Total Cases Evaluated:** 1,000 Patient Encounters
- **Average Length of Stay (LOS):** 107.5 minutes
- **Average Door-to-Doctor Time:** 43.4 minutes
- **Clinical Outlier Rate (IQR):** ~8.0% of total patient visits
- **Top Bottlenecks Identified:** 
  1. `Triage -> Lab Result` (Avg delay: 32.6 mins)
  2. `Registration -> Doctor Assessment` (Avg delay: 30.7 mins)

---

## 🛠️ Repository & Project Structure
```text
├── data/
│   └── processed_new/                 # Cleaned & feature-engineered event logs
├── notebooks/                         # Chronological analysis notebooks (Day 1 - Day 16)
│   ├── day01_setup_and_loading.ipynb
│   ├── day06_process_timeline.ipynb
│   ├── day11_outlier_detection.ipynb
│   └── day16_final_metrics_summary.ipynb
├── dashboard/                         # Power BI Analytics Dashboards
│   ├── CareFlow_Emergency_Dashboard.pbix         # Page 1: Overview Report
│   └── CareFlow_Process_and_Bottlenecks.pbix     # Page 2: Bottleneck Analytics
└── README.md                          # Main project documentation