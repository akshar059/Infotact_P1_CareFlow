
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_FILE = BASE_DIR / "docs" / "process_mining_insights_report.md"


def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return pd.read_csv(path)


def main():
    # Load existing analysis results
    frequency = load_csv("activity_frequency_summary.csv")
    pathways = load_csv("pathway_variation_summary.csv")
    loopbacks = load_csv("loopback_activity_summary.csv")
    waiting = load_csv("patient_waiting_time_summary.csv")
    journey = load_csv("patient_journey_comparison_summary.csv")
    performance = load_csv("workflow_performance_summary.csv")

    lines = [
        "# Day 19: Process Mining Insights and Findings Report",
        "",
        "## 1. Project Overview",
        "This report consolidates the process mining findings from the CareFlow "
        "clinical workflow dataset.",
        "",
        "## 2. Dataset Overview",
        "- Total patients analyzed: 1,000",
        "- Total recorded events: 6,964",
        "- Activity types: 10",
        "- Recorded transitions: 5,964",
        "",
        "## 3. Activity Frequency Findings",
        frequency.head(10).to_markdown(index=False),
        "",
        "## 4. Patient Pathway Findings",
        pathways.head(10).to_markdown(index=False),
        "",
        "## 5. Loopback Findings",
        loopbacks.head(10).to_markdown(index=False),
        "",
        "## 6. Waiting Time Findings",
        waiting.head(10).to_markdown(index=False),
        "",
        "## 7. Patient Journey Comparison",
        journey.head(10).to_markdown(index=False),
        "",
        "## 8. Workflow Performance Summary",
        performance.head(10).to_markdown(index=False),
        "",
        "## 9. Key Observations",
        "- Patient journeys follow multiple activity sequences.",
        "- Direct-discharge and investigation-based pathways have different durations.",
        "- Loopback events indicate repeated workflow activities.",
        "- Waiting-time summaries highlight transitions worth further investigation.",
        "- Elapsed time alone does not establish a clinical bottleneck.",
        "",
        "## 10. Improvement Opportunities",
        "- Review repeated triage and reassessment activities.",
        "- Investigate long-duration investigation pathways.",
        "- Review handoffs between investigation and documentation activities.",
        "- Monitor workflow variations to identify opportunities for improvement.",
        "",
        "## 11. Conclusion",
        "Process mining helps understand patient workflow patterns, pathway "
        "variations, repeated activities, and elapsed journey durations. "
        "These findings can support further workflow investigation and improvement.",
        "",
        "## 12. Scope and Limitations",
        "- Findings are based on the available recorded event data.",
        "- Elapsed journey duration is not necessarily actual waiting time.",
        "- Improvement opportunities require clinical and operational validation.",
    ]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("Day 19 insights report generated successfully.")
    print(f"Report saved: {REPORT_FILE}")
    print(f"Activity records: {len(frequency)}")
    print(f"Pathway records: {len(pathways)}")
    print(f"Loopback records: {len(loopbacks)}")
    print(f"Waiting-time records: {len(waiting)}")
    print(f"Journey comparison records: {len(journey)}")
    print(f"Performance records: {len(performance)}")


if __name__ == "__main__":
    main()
