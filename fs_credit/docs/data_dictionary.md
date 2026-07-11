# Data Dictionary — fs_credit

- **features.merchant_daily_cashflow**: Daily merchant aggregates (no PII).
- **features.events_chargeback**: Aggregated chargeback activity per merchant/day.
- **features.acquirer_features**: Risk and device/geo signals.
- **features.firmographics**: Bucketed firmographic attributes (static).
- **features.macro_signals**: Region-day macro indicators.

> All tables are PII-free, cohort-safe, and partitioned by `dt` where applicable.
