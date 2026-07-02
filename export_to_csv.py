import sqlite3
import pandas as pd
import os

# 1. Look directly inside the current folder instead of using '../'
db_path = 'bluestock_mf.db'
data_dir = 'data'

os.makedirs(data_dir, exist_ok=True)

if not os.path.exists(db_path):
    print(f"Error: Could not find '{db_path}' in the current directory!")
    print("Please make sure your .db file is located exactly in your blue_stock_project folder.")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch real tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"Found tables: {tables}")
    
    # Export them to the local data folder
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_csv(f"{data_dir}/{table}.csv", index=False)
        print(f"Successfully exported {table}.csv to {data_dir}/ folder!")
        
    conn.close()