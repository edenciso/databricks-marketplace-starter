# Databricks Marketplace Starter (Delta Sharing)

This repo contains two **Data + Model (+ UI)** bundles ready to publish on **Databricks Marketplace** using **Unity Catalog** + **Delta Sharing**:

- `fs_credit` — **SMB Cashflow Vector Risk Scoring** (Financial Services)
- `cpg_promo` — **Promo Lift Copilot** (Retail/CPG)

## Quick Start

1. **Create/choose a Unity Catalog catalog** for each solution (or use the suggested names in the SQL files).
2. In Databricks, open the `sql/01_create_tables.sql` for each solution and **run the DDL** to create tables.
3. Open the `notebooks/05_load_samples.py` notebook to **load synthetic sample data** into the created tables.
4. (Pro) Open the scoring notebook and **run end‑to‑end**.
5. (Studio) Open the Studio notebook and **walk through the UI workflow**.
6. Once validated, use files in `admin/delta_sharing` to set up **Shares/Recipients** and publish your **Marketplace listing**.

> All data here is **synthetic** and PII‑free. Adapt schemas, replace sample loaders with your production pipelines, and complete the model cards and governance docs.
