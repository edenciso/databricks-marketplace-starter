# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC ### Schema checksum

tables = ["features__merchant_daily_cashflow","features__events_chargeback","features__acquirer_features",
          "features__firmographics","features__macro_signals"]
for t in tables:
    df = spark.table(t).limit(1)
    print(t, sorted([f.name+':'+f.dataType.simpleString() for f in df.schema.fields]))
