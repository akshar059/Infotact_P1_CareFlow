
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = (
    ROOT / "data" / "processed" / "workflow_improvement_recommendations.csv"
)

# Load and validate the event dataset
df = pd.read_csv(DATA_FILE)

required = {"case_id", "activity_name", "timestamp", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

if df["timestamp"].isnull().any():
    raise ValueError("Invalid timestamps found in the dataset.")

df = df.sort_values(["case_id", "activity_order"]).copy()

# Identify consecutive activities
df["next_activity"] = df.groupby("case_id")["activity_name"].shift(-1)
df["next_timestamp"] = df.groupby("case_id")["timestamp"].shift(-1)

df["elapsed_minutes"] = (
    df["next_timestamp"] - df["timestamp"]
).dt.total_seconds() / 60

transitions = df.dropna(
    subset=["next_activity", "next_timestamp"]
).copy()

transitions = transitions[
    transitions["elapsed_minutes"] >= 0
].copy()

# Summarize transition frequency and elapsed time
summary = (
    transitions.groupby(["activity_name", "next_activity"])
    .agg(
        transition_count=("elapsed_minutes", "size"),
        average_elapsed_minutes=("elapsed_minutes", "mean"),
        median_elapsed_minutes=("elapsed_minutes", "median"),
    )
    .reset_index()
)

summary = summary.rename(columns={
    "activity_name": "from_activity",
    "next_activity": "to_activity",
})

# Recommendations are investigation suggestions, not confirmed causes
recommendation_map = {
    ("Lab Collection", "Lab Result"): (
        "Review laboratory sample transport, processing queues, "
        "and result recording timestamps.",
        "Track median and 90th-percentile elapsed time for lab results.",
    ),
    ("Triage", "Doctor Assessment"): (
        "Review patient queue patterns by hour and acuity before "
        "considering staffing or scheduling changes.",
        "Track elapsed time by hour and acuity, alongside median and 90th percentile.",
    ),
    ("X-Ray", "Radiology Result"): (
        "Review imaging queue, reporting workflow, and timestamp consistency.",
        "Track imaging-to-result elapsed time by department and time of day.",
    ),
    ("Documentation Review", "Discharge"): (
        "Review documentation completeness and discharge approval steps.",
        "Track documentation completion time and discharge turnaround.",
    ),
    ("Doctor Reassessment", "Discharge"): (
        "Review reassessment documentation and subsequent discharge steps.",
        "Track reassessment-to-discharge elapsed time and case counts.",
    ),
    ("Radiology Result", "Triage"): (
        "Review cases with this sequence to understand why triage occurs again.",
        "Track repeat-triage cases and review their documented reasons.",
    ),
}

records = []

for _, row in summary.iterrows():
    transition = (row["from_activity"], row["to_activity"])

    if transition in recommendation_map:
        recommendation, metric = recommendation_map[transition]
        priority = "High investigation priority"
    elif row["average_elapsed_minutes"] >= 15:
        recommendation = (
            "Review a sample of cases and validate timestamps before "
            "deciding whether workflow changes are needed."
        )
        metric = "Monitor case count, median elapsed time, and 90th percentile."
        priority = "Further review"
    else:
        recommendation = (
            "Continue monitoring transition frequency and elapsed time."
        )
        metric = "Monitor transition count and median elapsed time."
        priority = "Routine monitoring"

    records.append({
        "from_activity": row["from_activity"],
        "to_activity": row["to_activity"],
        "transition_count": int(row["transition_count"]),
        "average_elapsed_minutes": round(
            row["average_elapsed_minutes"], 2
        ),
        "median_elapsed_minutes": round(
            row["median_elapsed_minutes"], 2
        ),
        "investigation_priority": priority,
        "recommendation": recommendation,
        "suggested_metric": metric,
    })

recommendations = pd.DataFrame(records)

recommendations = recommendations.sort_values(
    ["investigation_priority", "average_elapsed_minutes"],
    ascending=[True, False],
).reset_index(drop=True)

recommendations.insert(0, "recommendation_id", range(1, len(recommendations) + 1))

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
recommendations.to_csv(OUTPUT_FILE, index=False)

print("=== WORKFLOW IMPROVEMENT RECOMMENDATIONS ===")
print(f"Patient cases: {df['case_id'].nunique()}")
print(f"Recorded events: {len(df)}")
print(f"Valid transitions analyzed: {len(transitions)}")
print(f"Recommendations generated: {len(recommendations)}")

print("\nTop 10 recommendations:")
print(recommendations.head(10).to_string(index=False))

print(f"\nResults saved to: {OUTPUT_FILE}")
print(
    "\nNote: Recommendations are for investigation. "
    "Elapsed time alone does not prove a bottleneck or its cause."
)
