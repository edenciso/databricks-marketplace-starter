# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC ### Sample uplift present (cpg_promo)

from pyspark.sql import functions as F
df = spark.table("temp__promo_uplift_latest")
assert df.count() > 0, "No uplift results"
assert df.filter(F.col("uplift_revenue").isNull()).count() == 0, "Null uplift detected"
print("OK: sample uplift exists and is non-null")
