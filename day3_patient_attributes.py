import os
import pandas as pd

# Dynamic path variable (so it's easy to swap datasets later if needed)
DATA_PATH = "data/cleaned_careflow.csv"
OUTPUT_PATH = "data/master_careflow_dataset.csv"

def process_day3_pipeline():
    print("--- Starting Day 3 Pipeline: Patient Attributes & Master Merging ---")
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: '{DATA_PATH}' file not found. Please check your data directory!")
        return

    # Load Cleaned Data
    df = pd.read_csv(DATA_PATH)
    print(f"Initial Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns.")

    # 1. Standardize Column Names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 2. Patient Attributes Cleaning & Format Standardizations
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    # 3. Missing Value Audit
    missing_counts = df.isnull().sum()
    print("\nMissing Values Summary:")
    print(missing_counts[missing_counts > 0] if missing_counts.sum() > 0 else "No missing values found!")

    # 4. Save Final Master Dataset
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Master Dataset successfully created at: '{OUTPUT_PATH}'")

if __name__ == "__main__":
    process_day3_pipeline()