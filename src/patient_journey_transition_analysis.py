
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "patient_journey_transition_summary.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Sort events in patient journey order
df = df.sort_values(["case_id", "activity_order"]).copy()

# Get each patient's current activity and next activity
df["next_activity"] = df.groupby("case_id")["activity_name"].shift(-1)

transitions = df.dropna(subset=["next_activity"]).copy()

# Count transitions between activities
summary = (
    transitions.groupby(["activity_name", "next_activity"])
    .size()
    .reset_index(name="transition_count")
)

total_transitions = len(transitions)

summary["percentage_of_transitions"] = (
    summary["transition_count"] / total_transitions * 100
).round(2)

summary = summary.rename(columns={
    "activity_name": "from_activity",
    "next_activity": "to_activity"
})

summary = summary.sort_values(
    "transition_count", ascending=False
).reset_index(drop=True)

summary.insert(0, "rank", range(1, len(summary) + 1))

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

# Display results
print("=== PATIENT JOURNEY TRANSITION ANALYSIS ===")
print(f"Total patient cases: {df['case_id'].nunique()}")
print(f"Total recorded events: {len(df)}")
print(f"Total consecutive transitions: {total_transitions}")
print(f"Unique transition types: {len(summary)}")

print("\nTop 10 transitions:")
print(summary.head(10).to_string(index=False))

print(f"\nResults saved to: {OUTPUT_FILE}")
