import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# 1. Setup configuration paths and database engine configurations
DB_PATH = "bluestock_mf.db"
SCHEMA_PATH = os.path.join("sql", "schema.sql")
PROCESSED_DIR = "data/processed"

engine = create_engine(f"sqlite:///{DB_PATH}")

print("Initializing relational star schema mappings within SQLite...")

# 2. Read and run schema.sql to initialize database structural architecture
if os.path.exists(SCHEMA_PATH):
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.close()
    print("✔ schema.sql applied successfully. Structural tables created.")
else:
    raise FileNotFoundError(f"Could not find schema.sql at location: {SCHEMA_PATH}")

# ==========================================
# LOAD DATA INTO TABLES
# ==========================================

# 1. Load dim_fund (from 01_fund_master_clean.csv)
print("Loading dim_fund table data...")
df_fund = pd.read_csv(os.path.join(PROCESSED_DIR, "01_fund_master_clean.csv"))
# Keep only columns defined in your SQL schema layout
fund_cols = ['amfi_code', 'fund_house', 'scheme_name', 'category', 'sub_category', 'plan', 'launch_date', 'min_sip_amount']
df_fund[fund_cols].to_sql("dim_fund", con=engine, if_exists="append", index=False)

# 2. Load fact_nav (from 02_nav_history_clean.csv)
print("Loading fact_nav table data (this may take a few moments)...")
df_nav = pd.read_csv(os.path.join(PROCESSED_DIR, "02_nav_history_clean.csv"))
df_nav[['amfi_code', 'date', 'nav']].to_sql("fact_nav", con=engine, if_exists="append", index=False)

# 3. Load fact_transactions (from 08_investor_transactions_clean.csv)
print("Loading fact_transactions table data...")
df_tx = pd.read_csv(os.path.join(PROCESSED_DIR, "08_investor_transactions_clean.csv"))
tx_cols = ['investor_id', 'transaction_date', 'amfi_code', 'transaction_type', 'amount_inr', 'city', 'state', 'kyc_status']
# Rename transaction_date if your dataframe uses a different naming pattern to line up with SQL columns
if 'transaction_date' not in df_tx.columns and 'date' in df_tx.columns:
    df_tx = df_tx.rename(columns={'date': 'transaction_date'})
df_tx[tx_cols].to_sql("fact_transactions", con=engine, if_exists="append", index=False)

# 4. Load fact_performance (from 07_scheme_performance_clean.csv)
print("Loading fact_performance table data...")
df_perf = pd.read_csv(os.path.join(PROCESSED_DIR, "07_scheme_performance_clean.csv"))
perf_cols = ['amfi_code', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct', 'sharpe_ratio']
df_perf[perf_cols].to_sql("fact_performance", con=engine, if_exists="append", index=False)

print("\n🎉 Database pipeline completed! 'bluestock_mf.db' is loaded and ready for queries.")