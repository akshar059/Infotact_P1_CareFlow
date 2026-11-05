# 🏥 CareFlow – Emergency Department Clinical Process Mining & Analytics

![Python](https://img.shields.io/badge/Python-Data%20Mining-blue)
![Power%20BI](https://img.shields.io/badge/Power%20BI-Analytics-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)

CareFlow is an end-to-end clinical process mining and analytics framework designed to evaluate patient throughput, identify operational bottlenecks, isolate duration outliers, and optimize resource allocation across Emergency Departments (ED).

---

## 👥 Project Team & Role Attribution

- **Member (Sagar Janathe):** Core Data Pipeline, Feature Engineering, Outlier & Anomaly Detection, Notebook Modules (Days 1–16), and Final Consolidated Analytics Deliverables[cite: 2, 6, 7].
- **Collaborating Team Members:** Process Mining Visualizations, Emergency Flow Overview, and Workload Analytics[cite: 2, 5].

---

## 📊 Primary Deliverables & Assets

| Asset Category | File / Path | Description |
| :--- | :--- | :--- |
| **Master Dashboard** | [`deliverables/CareFlow_Final_Analytics.pbix`](./deliverables/CareFlow_Final_Analytics.pbix)[cite: 6] | Consolidated multi-page Power BI report integrating all process mining modules |
| **Master Notebook** | [`deliverables/CareFlow_Master_EDA_Mining.ipynb`](./deliverables/CareFlow_Master_EDA_Mining.ipynb)[cite: 6] | Cleaned, leakage-free end-to-end data processing and clinical event log pipeline |
| **Executive Summary** | [`STAKEHOLDER_SUMMARY.md`](./STAKEHOLDER_SUMMARY.md)[cite: 2] | Strategic recommendations and high-level management findings |

---

## 📌 Key Clinical Findings & Metrics

- **Total Cases Evaluated:** 1,000 Patient Encounters[cite: 2]
- **Average Length of Stay (LOS):** 107.5 minutes[cite: 2]
- **Average Door-to-Doctor Time:** 43.4 minutes[cite: 2]
- **Clinical Outlier Rate (IQR):** ~8.0% of total patient visits[cite: 2]
- **Primary Bottlenecks Isolated:**
  - *Triage → Lab Result:* Average delay of 32.6 minutes[cite: 2]
  - *Registration → Doctor Assessment:* Average delay of 30.7 minutes[cite: 2]

---

## 📁 Repository Structure

```text
Infotact_P1_CareFlow/
├── dashboard/                              # Individual Power BI Report Pages[cite: 5]
│   ├── CareFlow_Doctors_and_Workloads.pbix[cite: 5]
│   ├── CareFlow_Emergency_Dashboard.pbix[cite: 5]
│   ├── CareFlow_Loopbacks_and_Outliers.pbix[cite: 5]
│   └── CareFlow_Process_and_Bottlenecks.pbix[cite: 5]
├── data/
│   └── processed_new/                      # Cleaned & feature-engineered event logs[cite: 2]
├── deliverables/                           # Master execution assets
│   ├── CareFlow_Final_Analytics.pbix       # Final merged Power BI dashboard
│   ├── CareFlow_Master_EDA_Mining.ipynb    # Consolidated pipeline notebook[cite: 6]
│   └── eda_and_dashboard_final.md[cite: 6]
├── notebooks/                              # Chronological analysis modules (Days 1–16)
│   ├── day3_eda_baseline.ipynb
│   ├── day11_outlier_and_anomaly_detection.ipynb
│   └── day16_final_metrics_summary.ipynb[cite: 7]
├── README.md                               # Main project documentation[cite: 2]
└── STAKEHOLDER_SUMMARY.md                  # Executive insights & strategy[cite: 2]