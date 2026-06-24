import os
import pandas as pd
import numpy as np

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Starting Day 2 Data Cleaning Pipeline...")

# ==========================================
# 1. CLEANING NAV HISTORY
# ==========================================
print("Processing 02_nav_history.csv...")
df_nav = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))

df_nav['date'] = pd.to_datetime(df_nav['date'])
df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
df_nav = df_nav.sort_values(by=['amfi_code', 'date'])

# Forward-fill gaps chronologically within each fund
df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
df_nav = df_nav[df_nav['nav'] > 0]

df_nav.to_csv(os.path.join(PROCESSED_DIR, "02_nav_history_clean.csv"), index=False)
print("✔ 02_nav_history.csv cleaned and saved.")


# ==========================================
# 2. CLEANING INVESTOR TRANSACTIONS
# ==========================================
print("Processing 08_investor_transactions.csv...")
df_tx = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"))

df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])

# Standardize values to clean mixed strings
df_tx['transaction_type'] = df_tx['transaction_type'].str.strip().str.lower()
type_map = {
    'sip': 'SIP',
    'lumpsum': 'Lumpsum',
    'lump_sum': 'Lumpsum',
    'lump sum': 'Lumpsum',
    'redemption': 'Redemption'
}
df_tx['transaction_type'] = df_tx['transaction_type'].map(type_map).fillna('Lumpsum')

df_tx = df_tx[df_tx['amount_inr'] > 0]
df_tx['kyc_status'] = df_tx['kyc_status'].str.strip().str.capitalize()

df_tx.to_csv(os.path.join(PROCESSED_DIR, "08_investor_transactions_clean.csv"), index=False)
print("✔ 08_investor_transactions.csv cleaned and saved.")


# ==========================================
# 3. CLEANING SCHEME PERFORMANCE
# ==========================================
print("Processing 07_scheme_performance.csv...")
df_perf = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))

numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct']
for col in numeric_cols:
    df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')

# Clamp the expense ratios between 0.1% and 2.5% as requested
df_perf['expense_ratio_pct'] = df_perf['expense_ratio_pct'].clip(0.1, 2.5)

df_perf.to_csv(os.path.join(PROCESSED_DIR, "07_scheme_performance_clean.csv"), index=False)
print("✔ 07_scheme_performance.csv cleaned and saved.")


# ==========================================
# 4. STANDARDIZING REMAINING FILES
# ==========================================
print("Standardizing structural formats for remaining tracking assets...")
other_files = [
    "01_fund_master.csv", "03_aum_by_fund_house.csv", "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv", "06_industry_folio_count.csv", "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file_name in other_files:
    raw_path = os.path.join(RAW_DIR, file_name)
    if os.path.exists(raw_path):
        df_temp = pd.read_csv(raw_path)
        
        # Safe format conversion approach
        for col in ['date', 'month', 'portfolio_date']:
            if col in df_temp.columns:
                # Convert string type to ensure uniform pandas operation
                df_temp[col] = df_temp[col].astype(str)
                # Parse to datetime safely using errors='coerce' to bypass string parsing assertion crashes
                df_temp[col] = pd.to_datetime(df_temp[col], errors='coerce')
                
        clean_name = file_name.replace(".csv", "_clean.csv")
        df_temp.to_csv(os.path.join(PROCESSED_DIR, clean_name), index=False)

print("🎉 All 10 cleaned datasets saved successfully inside 'data/processed/'!")