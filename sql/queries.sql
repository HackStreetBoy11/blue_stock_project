-- sql/queries.sql
-- ==============================================================================
-- BLUESTOCK MUTUAL FUND PLATFORM: 10 ANALYTICAL SQL QUERIES
-- ==============================================================================

-- 1. Top 5 Funds by Total Transaction Inflows
SELECT f.scheme_name, SUM(t.amount_inr) as total_inflow
FROM fact_transactions t
    JOIN dim_fund f ON t.amfi_code = f.amfi_code
WHERE t.transaction_type != 'Redemption'
GROUP BY f.scheme_name
ORDER BY total_inflow DESC
LIMIT 5;

-- 2. Average Historical NAV tracking per month per fund
SELECT amfi_code
, strftime
('%Y-%m', date) as active_month, AVG
(nav) as average_nav
FROM fact_nav
GROUP BY amfi_code, active_month
ORDER BY active_month ASC;

-- 3. Total Transaction Volume distributions separated by State lines
SELECT state, COUNT(*) as transaction_count, SUM(amount_inr) as gross_volume
FROM fact_transactions
GROUP BY state
ORDER BY gross_volume DESC;

-- 4. Active Portfolio Target Schemes holding an Expense Ratio lower than 1%
SELECT f.scheme_name, p.expense_ratio_pct
FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;

-- 5. Ratio of SIP vs Lumpsum transactions
SELECT transaction_type, COUNT(*) as count, SUM(amount_inr) as gross_capital
FROM fact_transactions
GROUP BY transaction_type;

-- 6. Top 5 Funds with the Highest 3-Year CAGR Returns
SELECT f.scheme_name, f.fund_house, p.return_3yr_pct
FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_3yr_pct IS NOT NULL
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 7. Total Outflow (Redemptions) per City Tier
SELECT t
.city_tier, COUNT
(*) as redemption_count, SUM
(t.amount_inr) as total_outflow
FROM fact_transactions t
WHERE t.transaction_type = 'Redemption'
GROUP BY t.city_tier
ORDER BY total_outflow DESC;

-- 8. High-Value Investors (Total Investment > 500,000 INR)
SELECT investor_id, kyc_status, COUNT(*) as total_txs, SUM(amount_inr) as aggregate_capital
FROM fact_transactions
WHERE transaction_type != 'Redemption'
GROUP BY investor_id, kyc_status
HAVING aggregate_capital > 500000
ORDER BY aggregate_capital DESC;

-- 9. Risk-Adjusted Return Analysis (Top Funds by Sharpe Ratio)
SELECT f.scheme_name, f.category, p.sharpe_ratio, p.return_5yr_pct
FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.sharpe_ratio IS NOT NULL
ORDER BY p.sharpe_ratio DESC
LIMIT 5;

-- 10. Investor Demographics Breakdown by Gender and KYC Status
SELECT gender
, kyc_status, COUNT
(DISTINCT investor_id) as total_unique_investors, SUM
(amount_inr) as transaction_volume
FROM fact_transactions
GROUP BY gender, kyc_status
ORDER BY transaction_volume DESC;