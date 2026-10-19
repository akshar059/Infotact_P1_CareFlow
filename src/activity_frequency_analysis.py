
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "activity_frequency_summary.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Sort activities within each patient case
df = df.sort_values(["case_id", "activity_order"]).copy()

total_cases = df["case_id"].nunique()

# Summarize activity frequency
summary = (
    df.groupby("activity_name")
    .agg(
        event_count=("activity_name", "size"),
        unique_cases=("case_id", "nunique"),
    )
    .reset_index()
)

summary["percentage_of_events"] = (
    summary["event_count"] / len(df) * 100
).round(2)

summary["percentage_of_cases"] = (
    summary["unique_cases"] / total_cases * 100
).round(2)

# Count repeated occurrences after the first occurrence per case
df["occurrence_number"] = (
    df.groupby(["case_id", "activity_name"]).cumcount() + 1
)

repeat_summary = (
    df[df["occurrence_number"] > 1]
    .groupby("activity_name")
    .size()
    .reset_index(name="repeat_event_count")
)

summary = summary.merge(repeat_summary, on="activity_name", how="left")
summary["repeat_event_count"] = (
    summary["repeat_event_count"].fillna(0).astype(int)
)

summary = summary.sort_values("event_count", ascending=False)

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

print("=== ACTIVITY FREQUENCY ANALYSIS ===")
print(f"Total patient cases: {total_cases}")
print(f"Total recorded events: {len(df)}")
print(f"Unique activity types: {df['activity_name'].nunique()}")

print("\nActivity frequency ranking:")
print(summary.to_string(index=False))

print(f"\nResults saved to: {OUTPUT_FILE}")
