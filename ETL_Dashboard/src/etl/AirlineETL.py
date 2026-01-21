import sys
import os
import pandas as pd
import sqlite3
import kagglehub

# Ensure the 'src' directory is in the python path
current_dir = os.path.dirname(os.path.abspath(__file__)) # etl folder
src_dir = os.path.dirname(current_dir) # src folder
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Now try the import again
try:
    from backend.backend import DB_PATH, TABLE_NAME
except ImportError as e:
    print(f"Import Error: {e}")
    print("Check that DB_PATH is defined inside src/backend/backend.py")
    sys.exit(1)

def run_etl():
    print("Step 1: Downloading from Kaggle...")
    try:
        path = kagglehub.dataset_download("iamsouravbanerjee/airline-dataset")
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
        df = pd.read_csv(os.path.join(path, files[0]))
    except Exception as e:
        print(f"Kaggle Error: {e}")
        return

    print("Step 2: Transforming...")
    df.columns = [c.strip().replace(' ', '_').lower() for c in df.columns]
    df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(0)
    df['departure_date'] = pd.to_datetime(df['departure_date'], errors='coerce')
    
    # Required business logic for your project
    df['is_delayed'] = df['flight_status'].apply(lambda x: 1 if x == 'Delayed' else 0)

    print(f"Step 3: Loading into {DB_PATH}...")
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    print("--- ETL SUCCESSFUL ---")

if __name__ == "__main__":
    run_etl()