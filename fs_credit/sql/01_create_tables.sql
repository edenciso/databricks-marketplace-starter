-- Adjust the catalog name as needed
USE CATALOG catalog;
CREATE SCHEMA IF NOT EXISTS fs_credit;
USE SCHEMA fs_credit;

CREATE TABLE IF NOT EXISTS features__merchant_daily_cashflow (
  dt DATE,
  merchant_id STRING,
  mcc STRING,
  region STRING,
  tx_count BIGINT,
  gross_volume DOUBLE,
  net_volume DOUBLE,
  avg_ticket DOUBLE,
  refunds_count BIGINT,
  chargebacks_count BIGINT,
  auth_decline_rate DOUBLE,
  tenure_days INT,
  dow INT,
  dom INT,
  holiday_flag BOOLEAN
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__events_chargeback (
  dt DATE,
  merchant_id STRING,
  cb_count BIGINT,
  cb_amt DOUBLE,
  cb_win_rate DOUBLE
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__acquirer_features (
  dt DATE,
  merchant_id STRING,
  risk_flag BOOLEAN,
  velocity_alerts INT,
  device_fingerprint_count INT,
  ip_geo_mismatch_rate DOUBLE
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__firmographics (
  merchant_id STRING,
  entity_age_bucket STRING,
  employees_bucket STRING,
  est_revenue_bucket STRING,
  industry_bucket STRING
);

CREATE TABLE IF NOT EXISTS features__macro_signals (
  dt DATE,
  region STRING,
  unemployment_rate DOUBLE,
  retail_index DOUBLE,
  smallbiz_sentiment DOUBLE
)
PARTITIONED BY (dt);
