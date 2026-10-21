
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "patient_journey_sequence_summary.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Sort activities in each patient journey
df = df.sort_values(["case_id", "activity_order"])

# Create one activity sequence for each patient
journeys = (
    df.groupby("case_id")["activity_name"]
    .agg(list)
    .reset_index(name="activities")
)

journeys["activity_sequence"] = journeys["activities"].apply(
    lambda activities: " -> ".join(activities)
)

# Count complete journey sequences
summary = (
    journeys.groupby("activity_sequence")
    .agg(
        patient_count=("case_id", "count"),
        activity_count=("activities", lambda x: len(x.iloc[0]))
    )
    .reset_index()
)

total_patients = journeys["case_id"].nunique()

summary["percentage_of_patients"] = (
    summary["patient_count"] / total_patients * 100
).round(2)

summary = summary.sort_values(
    "patient_count", ascending=False
).reset_index(drop=True)

# Add rank
summary.insert(0, "rank", range(1, len(summary) + 1))

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

# Display results
print("=== PATIENT JOURNEY SEQUENCE ANALYSIS ===")
print(f"Total patients: {total_patients}")
print(f"Total recorded events: {len(df)}")
print(f"Unique complete journey sequences: {len(summary)}")

print("\nTop 10 patient journey sequences:")
print(summary.head(10).to_string(index=False))

print(f"\nResults saved to: {OUTPUT_FILE}")

