import os
import pandas as pd
import sqlite3
import kagglehub

# --- SHARED CONFIGURATION ---
DB_FILE = "airline_operations.db"
TABLE_NAME = "flight_data"

def run_etl():
    """ [Initials] Extracts from Kaggle, transforms, and loads into SQLite. """
    
    # 1. EXTRACT (Kaggle Download)
    print("Step 1: Downloading dataset from Kaggle...")
    try:
        # Dataset handle from the URL you provided
        path = kagglehub.dataset_download("iamsouravbanerjee/airline-dataset")
        
        # Find the CSV file in the downloaded path
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        if not files:
            print("No CSV found in Kaggle download.")
            return
            
        csv_path = os.path.join(path, files[0])
        df = pd.read_csv(csv_path)
        print(f"Successfully extracted {len(df)} rows.")
    except Exception as e:
        print(f"Kaggle Download Failed: {e}")
        return

    # 2. TRANSFORM
    print("Step 2: Transforming Data...")
    # Standardize column names for SQL
    df.columns = [c.replace(' ', '_').lower() for c in df.columns]
    
    # Cleaning
    df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')
    df = df.fillna({'flight_status': 'Unknown', 'age': 0})
    
    # Business Logic: Create a delay flag
    df['is_delayed'] = df['flight_status'].apply(lambda x: 1 if x == 'Delayed' else 0)

    # 3. LOAD
    print(f"Step 3: Loading into Database table '{TABLE_NAME}'...")
    try:
        with sqlite3.connect(DB_FILE) as conn:
            df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
        print("--- ETL PROCESS SUCCESSFUL ---")
    except Exception as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    run_etl()