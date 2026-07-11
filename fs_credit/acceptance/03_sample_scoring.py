# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC ### Sample scoring returns non-null probabilities

from pyspark.sql import functions as F
df = spark.table("temp__scores_latest")
assert df.count() > 0, "No scores written"
assert df.filter(F.col("pd").isNull()).count() == 0, "Null PD scores present"
print("OK: sample scores exist and are non-null")
