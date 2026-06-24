# Day 1: Data Quality & Structural Summary

## 1. Dataset Profiles
* **01_fund_master.csv**: 40 rows, 15 columns. Key attributes: amfi_code, fund_house, scheme_name, category, asset details.
* **02_nav_history.csv**: 46,000 rows, 3 columns. Key attributes: amfi_code, date, nav (historical pricing records).
* **03_aum_by_fund_house.csv**: 90 rows, 5 columns. Tracks periodic asset allocation (AUM) values across target fund houses.
* **04_monthly_sip_inflows.csv**: 48 rows, 6 columns. Contains transactional metrics detailing systematic investment plan inflows.
* **05_category_inflows.csv**: 144 rows, 3 columns. Summarizes historical directional capital inflows sorted by market capitalization groupings.
* **06_industry_folio_count.csv**: 21 rows, 6 columns. Measures historical growth trends across active mutual fund folio registrations.
* **07_scheme_performance.csv**: 40 rows, 19 columns. Comprehensive performance benchmarks, alpha, beta, and risk ratings.
* **08_investor_transactions.csv**: 32,778 rows, 13 columns. Granular investor transaction history logging payment types, amounts, and demographic metrics.
* **09_portfolio_holdings.csv**: 322 rows, 8 columns. Individual underlying asset holding weights, sectoral profiles, and stock targets.
* **10_benchmark_indices.csv**: 8,050 rows, 3 columns. Core foundational market reference points (e.g., NIFTY50) tracking comparative values over time.

## 2. AMFI Code Validation Results
* **Total Unique Schemes in Master:** 40
* **Unique Codes in NAV History:** 40
* **Validation Status:** SUCCESS
* **Findings:** The script executed a complete relational cross-reference loop. Confirmed that 100% of the 40 unique scheme codes present in the fund master map perfectly to their historical records inside the transactional dataset. Zero orphaned codes or broken integrity links were detected.

## 3. Anomalies Noted
* **Missing Data Identified:** A minor alert was logged during structural profile scanning showing 12 missing entries inside `04_monthly_sip_inflows.csv` (yoy_growth_pct). 
* **Data Typings Integrity:** Aside from expected trailing NaN data points, all field properties match correctly. Data columns successfully resolved to numeric schemas (`int64`, `float64`) and categorical features (`object`), validating structural readiness for database mapping.