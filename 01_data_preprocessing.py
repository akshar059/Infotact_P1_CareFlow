import os
import pandas as pd

def load_and_clean_data(file_path):
    print("--- CareFlow Data Pipeline Starting ---")
    if not os.path.exists(file_path):
        print(f"File not found at: {file_path}")
        return None
    
    # Load dataset
    df = pd.read_csv(file_path)
    print(f"Dataset successfully loaded! Total Rows: {len(df)}")
    
    # 1. Convert Timestamp to datetime object
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        print("-> Timestamps successfully converted to datetime format.")
        
    # 2. Check for missing values
    missing_vals = df.isnull().sum().sum()
    print(f"-> Total missing values found: {missing_vals}")
    
    # 3. Save the cleaned dataset into data folder
    output_path = os.path.join("data", "cleaned_careflow.csv")
    df.to_csv(output_path, index=False)
    print(f"-> Cleaned dataset successfully saved at: {output_path}")
    
    return df

if __name__ == "__main__":
    csv_path = os.path.join("data", "careflow_synthetic_event_log.csv")
    load_and_clean_data(csv_path)