CREATE DATABASE valuation_db;
CREATE USER app_user WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE valuation_db TO app_user;

CREATE TABLE valuations (
    id BIGSERIAL PRIMARY KEY,
    company TEXT NOT NULL,
    asset_value REAL,
    earnings_power_value REAL,
    wacc REAL,
    value_per_share REAL,
    margin_of_safety REAL,
    business_category TEXT,
    valuation_date TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE staging (
    id BIGSERIAL PRIMARY KEY,
    ticker TEXT,
    "name" TEXT,
    number_of_shares TEXT,
    current_assets TEXT,
    non_current_assets TEXT,
    current_liabilities TEXT,
    non_current_liabilities TEXT,
    total_equity TEXT,
    r_and_d TEXT,
    admin_expenses TEXT,
    tangibles TEXT,
    depreciation_and_amortization TEXT,
    turnover TEXT,
    operating_margin_5y_av TEXT,
    ebit_5y_av TEXT,
    tax_rate_paid_5y_av TEXT,
    non_current_assets_5_y_av TEXT,
    turnover_5y_av TEXT,
    turnover_perc_chg TEXT,
    borrowing TEXT,
    leases TEXT,
    debt TEXT,
    beta TEXT,
    cash TEXT,
    "close" TEXT,
    capex_5y_av TEXT,
    r_and_d_5y_av TEXT,
    admin_expenses_5y_av TEXT,
    data_extract_date TEXT,
    upload_date TIMESTAMP DEFAULT current_timestamp
);