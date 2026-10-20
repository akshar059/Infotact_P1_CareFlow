from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "activity_distribution_summary.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Validate required columns
required = {"case_id", "activity_name"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df[list(required)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# Calculate total cases and events
total_cases = df["case_id"].nunique()
total_events = len(df)

# Analyze activity distribution
summary = (
    df.groupby("activity_name")
    .agg(
        event_count=("activity_name", "size"),
        unique_patients=("case_id", "nunique")
    )
    .reset_index()
)

# Calculate percentages
summary["percentage_of_events"] = (
    summary["event_count"] / total_events * 100
).round(2)

summary["percentage_of_patients"] = (
    summary["unique_patients"] / total_cases * 100
).round(2)

# Sort by number of patients
summary = summary.sort_values(
    "unique_patients", ascending=False
)

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

# Display results
print("=== PATIENT ACTIVITY DISTRIBUTION ANALYSIS ===")
print(f"Total patient cases: {total_cases}")
print(f"Total recorded events: {total_events}")
print(f"Unique activity types: {df['activity_name'].nunique()}")

print("\nActivity distribution:")
print(summary.to_string(index=False))

print(f"\nResults saved to: {OUTPUT_FILE}")