# BlueStock Mutual Fund Platform Data Dictionary

This data dictionary documents the production database layout implemented inside `bluestock_mf.db`. The system is designed using a **Star Schema** to separate core dimensional lookups from transactional ledger tracking entries.

---

## 1. Dimension Tables

### Table: `dim_fund`
Description: Central lookup index containing structural attributes and metadata for the 40 core tracked mutual fund schemes.

| Column Name | Data Type | Key Type | Business Definition | Source Reference / Rules |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key | Unique 6-digit asset identifier code issued by AMFI. | `01_fund_master.csv` |
| `fund_house` | TEXT | None | The Asset Management Company (AMC) managing the fund pool. | Required (`NOT NULL`) |
| `scheme_name` | TEXT | None | Full public commercial name of the mutual fund asset pool. | Required (`NOT NULL`) |
| `category` | TEXT | None | High-level asset classification (e.g., Equity, Debt, Hybrid). | Raw Metadata |
| `sub_category`| TEXT | None | Granular strategy designation (e.g., Large Cap, Flexi Cap). | Raw Metadata |
| `plan` | TEXT | None | Entry structure configuration (e.g., Regular Plan, Direct Plan).| Raw Metadata |
| `launch_date` | TEXT | None | The operational inception date of the fund. | Parsed String |
| `min_sip_amount`| REAL | None | Minimum investment boundary allowed for monthly systematic plans.| Numerical Limit |

---

## 2. Fact Tables

### Table: `fact_nav`
Description: High-volume ledger recording chronological daily historical Net Asset Value pricing metrics.

| Column Name | Data Type | Key Type | Business Definition | Source Reference / Rules |
| :--- | :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incrementing internal table sequence entry identifier. | Generated (`AUTOINCREMENT`) |
| `amfi_code` | INTEGER | Foreign Key | Linked reference mapping records back to the master `dim_fund`. | References `dim_fund(amfi_code)` |
| `date` | TEXT | None | The market trading evaluation date. | Parsed ISO String (`YYYY-MM-DD`) |
| `nav` | REAL | None | Calculated closing valuation price point per mutual fund unit. | Verified > 0 / Forward-filled |

### Table: `fact_transactions`
Description: Granular ledger logging historical investor purchases, subscription actions, and cash outflows.

| Column Name | Data Type | Key Type | Business Definition | Source Reference / Rules |
| :--- | :--- | :--- | :--- | :--- |
| `transaction_id`| INTEGER | Primary Key | Auto-incrementing tracking transaction ledger entry index. | Generated (`AUTOINCREMENT`) |
| `investor_id` | TEXT | None | Unique system hashing tracking ID mapping back to an investor. | Masked String |
| `transaction_date`| TEXT| None | The explicit calendar date when capital deployment settled. | Parsed ISO String (`YYYY-MM-DD`) |
| `amfi_code` | INTEGER | Foreign Key | The target mutual fund asset code selected by the investor. | References `dim_fund(amfi_code)` |
| `transaction_type`| TEXT | None | Standardized categorization: `SIP`, `Lumpsum`, `Redemption`.| Mapped Enum Strings |
| `amount_inr` | REAL | None | Total structural local currency capital volume exchanged. | Verified > 0 |
| `city` | TEXT | None | Origin settlement city location of the trading individual. | Demographics |
| `state` | TEXT | None | Origin geographic fallback state boundary indicator. | Demographics |
| `kyc_status` | TEXT | None | Know Your Customer validation level (e.g., Verified, Pending).| Sentence-cased Enum |

### Table: `fact_performance`
Description: Analytical risk metrics matrix detailing trailing investment yields and alpha/beta indices.

| Column Name | Data Type | Key Type | Business Definition | Source Reference / Rules |
| :--- | :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary / FK | Unique asset identifier tracking entry back to `dim_fund`. | References `dim_fund(amfi_code)` |
| `return_1yr_pct`| REAL | None | Trailing 12-month compounding growth rate percentage yield. | Forced Numeric (`NaN` clean) |
| `return_3yr_pct`| REAL | None | Trailing 3-year annualized compound asset output growth profile. | Forced Numeric (`NaN` clean) |
| `return_5yr_pct`| REAL | None | Trailing 5-year annualized strategic compound asset performance. | Forced Numeric (`NaN` clean) |
| `expense_ratio_pct`| REAL | None | Management operating cost fee deduction slice assessed by AMC. | Clamped Range: `0.1% - 2.5%` |
| `sharpe_ratio` | REAL | None | Core historical baseline asset risk-to-reward ratio measure. | Volatility Index Metric |