# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Pro — Batch Scoring (fs_credit)

# COMMAND ----------
import mlflow, pandas as pd
from pyspark.sql import functions as F

catalog="catalog"; schema="fs_credit"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

features = (spark.table("features__merchant_daily_cashflow")
  .join(spark.table("features__events_chargeback"), ["merchant_id","dt"], "left")
  .join(spark.table("features__acquirer_features"), ["merchant_id","dt"], "left")
  .join(spark.table("features__firmographics"), ["merchant_id"], "left")
  .join(spark.table("features__macro_signals"), ["dt","region"], "left"))

scoring_day = spark.sql("SELECT max(dt) AS dt FROM features__merchant_daily_cashflow").first()["dt"]
X = features.filter(F.col("dt")==scoring_day).toPandas()

# Placeholder model: random scores. Replace with MLflow model load in production.
import numpy as np
pd_scores = pd.DataFrame({"merchant_id": X["merchant_id"], "pd": np.clip(np.random.beta(2,8, size=len(X)),0,1)})
spark.createDataFrame(pd_scores).write.mode("overwrite").saveAsTable("temp__scores_latest")

display(spark.table("temp__scores_latest").limit(10))
