from pathlib import Path
import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load the final dataset
df = pd.read_csv(INPUT_FILE)

# 2. Check required columns
required_columns = {"case_id", "activity_name", "activity_order"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")

if df[list(required_columns)].isnull().any().any():
    raise ValueError("Missing values found in required columns.")

# 3. Sort activities in patient workflow order
df = df.sort_values(["case_id", "activity_order"]).copy()

# 4. Find the next activity for each patient case
df["next_activity"] = (
    df.groupby("case_id")["activity_name"].shift(-1)
)

# 5. Keep consecutive activity transitions
transitions = df.dropna(subset=["next_activity"]).copy()

transitions["transition"] = (
    transitions["activity_name"]
    + " -> "
    + transitions["next_activity"]
)

# Save individual transitions
transitions.to_csv(
    OUTPUT_DIR / "activity_transition_details.csv",
    index=False,
)

# 6. Count how often each transition occurs
transition_summary = (
    transitions.groupby("transition")
    .size()
    .reset_index(name="transition_count")
    .sort_values("transition_count", ascending=False)
)

# Save transition summary
transition_summary.to_csv(
    OUTPUT_DIR / "activity_transition_summary.csv",
    index=False,
)

# 7. Display results
print("=== ACTIVITY TRANSITION ANALYSIS ===")
print(f"Total events: {len(df)}")
print(f"Total transitions: {len(transitions)}")
print(f"Unique transition types: {len(transition_summary)}")

print("\nMost common activity transitions:")
print(transition_summary.head(10).to_string(index=False))

print("\nAnalysis completed successfully!")
print(f"Results saved in: {OUTPUT_DIR}")