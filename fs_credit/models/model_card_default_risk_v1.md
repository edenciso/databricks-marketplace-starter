# Model Card — default_risk_v1

**Intended Use**: Estimate probability of default for SMB merchants using aggregated cashflow and risk features.
**Algorithm**: Gradient boosted trees.
**Training Data**: Aggregated transactional features (no PII). Include macro joins.
**Metrics**: AUC, KS; calibration plot in notebook.
**Limitations**: Not a guarantee of future performance; monitor drift.
**Fairness/Bias**: Exclude protected-class proxies; audit SHAP reason codes.
**Retrain Cadence**: Monthly.
