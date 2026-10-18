
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "raw" / "careflow_events_scaled.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "pathway_variation_summary.csv"

# Load the dataset
df = pd.read_csv(DATA_FILE)

# Check required columns
required = {"case_id", "activity_name", "activity_order"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

# Remove rows with missing pathway information
df = df.dropna(subset=["case_id", "activity_name", "activity_order"])

# Sort activities in each patient case
df = df.sort_values(["case_id", "activity_order"])

# Create one activity sequence per patient case
pathways = (
    df.groupby("case_id")["activity_name"]
    .agg(list)
    .reset_index(name="activities")
)

pathways["pathway"] = pathways["activities"].apply(
    lambda activities: " -> ".join(map(str, activities))
)

# Count cases following each exact sequence
summary = (
    pathways.groupby("pathway")
    .size()
    .reset_index(name="case_count")
    .sort_values("case_count", ascending=False)
)

summary["percentage"] = (
    summary["case_count"] / pathways["case_id"].nunique() * 100
).round(2)

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary.to_csv(OUTPUT_FILE, index=False)

print("=== PATIENT PATHWAY VARIATION ANALYSIS ===")
print(f"Total patient cases: {pathways['case_id'].nunique()}")
print(f"Unique pathways: {len(summary)}")
print("\nTop 10 most common pathways:")
print(summary.head(10).to_string(index=False))
print(f"\nResults saved to: {OUTPUT_FILE}")
