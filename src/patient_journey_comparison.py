
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATA_FILE = BASE_DIR / "data" / "raw" / "careflow_events_scaled.csv"

OUTPUT_FILE = PROCESSED_DIR / "patient_journey_comparison_summary.csv"
REPORT_FILE = BASE_DIR / "docs" / "patient_journey_comparison.md"


def main():
    events = pd.read_csv(DATA_FILE)
    events["timestamp"] = pd.to_datetime(events["timestamp"])

    events = events.sort_values(["case_id", "activity_order"])

    journeys = events.groupby("case_id").agg(
        first_activity=("timestamp", "min"),
        last_activity=("timestamp", "max"),
    )

    journeys["journey_duration_minutes"] = (
        journeys["last_activity"] - journeys["first_activity"]
    ).dt.total_seconds() / 60

    sequences = (
        events.groupby("case_id")["activity_name"]
        .agg(lambda activities: " -> ".join(activities.astype(str)))
        .rename("activity_sequence")
    )

    comparison = journeys.join(sequences).reset_index()

    summary = (
        comparison.groupby("activity_sequence")
        .agg(
            patient_count=("case_id", "nunique"),
            average_journey_duration_minutes=(
                "journey_duration_minutes", "mean"
            ),
            minimum_journey_duration_minutes=(
                "journey_duration_minutes", "min"
            ),
            maximum_journey_duration_minutes=(
                "journey_duration_minutes", "max"
            ),
        )
        .reset_index()
        .sort_values("patient_count", ascending=False)
    )

    total_patients = comparison["case_id"].nunique()

    summary["percentage_of_patients"] = (
        summary["patient_count"] / total_patients * 100
    ).round(2)

    duration_columns = [
        "average_journey_duration_minutes",
        "minimum_journey_duration_minutes",
        "maximum_journey_duration_minutes",
    ]
    summary[duration_columns] = summary[duration_columns].round(2)

    summary.to_csv(OUTPUT_FILE, index=False)

    report = [
        "# Day 18: Patient Journey Comparison Analysis",
        "",
        "## Objective",
        "Compare complete patient pathways by frequency and journey duration.",
        "",
        "## Dataset Summary",
        f"- Patients analyzed: {total_patients}",
        f"- Unique pathways: {len(summary)}",
        f"- Total events: {len(events)}",
        "",
        "## Pathway Comparison",
        "",
        summary.to_markdown(index=False),
        "",
        "## Interpretation",
        "- Patient count indicates how frequently each pathway occurs.",
        "- Average journey duration measures elapsed time from first to last recorded event.",
        "- Minimum and maximum show the observed duration range.",
        "- Longer elapsed duration alone does not prove a clinical bottleneck.",
        "",
        "## Output",
        f"- `{OUTPUT_FILE.relative_to(BASE_DIR)}`",
    ]

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("Patient journey comparison analysis completed.")
    print(f"Patients analyzed: {total_patients}")
    print(f"Unique pathways: {len(summary)}")
    print(f"CSV saved: {OUTPUT_FILE}")
    print(f"Report saved: {REPORT_FILE}")
    print("\nTop 5 pathways:")
    print(summary.head().to_string(index=False))


if __name__ == "__main__":
    main()
