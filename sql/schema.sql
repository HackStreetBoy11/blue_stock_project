-- schema.sql
-- Drop tables if they exist to allow clean iterative re-runs
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS dim_fund;

-- 1. Create Dimension Tables
CREATE TABLE dim_fund
(
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    min_sip_amount REAL
);

    -- 2. Create Fact Tables incorporating Foreign Key constraints mapping back to Master Dimensions
    CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY
    (amfi_code) REFERENCES dim_fund
    (amfi_code)
);

    CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount_inr REAL,
    city TEXT,
    state TEXT,
    kyc_status TEXT,
    FOREIGN KEY
    (amfi_code) REFERENCES dim_fund
    (amfi_code)
);

    CREATE TABLE fact_performance
    (
        amfi_code INTEGER PRIMARY KEY,
        return_1yr_pct REAL,
        return_3yr_pct REAL,
        return_5yr_pct REAL,
        expense_ratio_pct REAL,
        sharpe_ratio REAL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );