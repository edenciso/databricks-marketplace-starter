-- Provider-side Delta Sharing templates (adjust names/paths)
USE CATALOG catalog;
CREATE SHARE IF NOT EXISTS fs_credit_share;
ALTER SHARE fs_credit_share ADD TABLE catalog.fs_credit.features__merchant_daily_cashflow;
ALTER SHARE fs_credit_share ADD TABLE catalog.fs_credit.features__events_chargeback;
ALTER SHARE fs_credit_share ADD TABLE catalog.fs_credit.features__acquirer_features;
ALTER SHARE fs_credit_share ADD TABLE catalog.fs_credit.features__firmographics;
ALTER SHARE fs_credit_share ADD TABLE catalog.fs_credit.features__macro_signals;

-- CREATE RECIPIENT my_consumer USING IDENTITY '...';
-- GRANT USAGE ON SHARE fs_credit_share TO RECIPIENT my_consumer;
