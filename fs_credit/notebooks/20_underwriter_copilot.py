# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Studio — Underwriter Copilot (fs_credit)

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window

catalog="catalog"; schema="fs_credit"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

scores = spark.table("temp__scores_latest")
threshold = float(dbutils.widgets.get("PD_THRESHOLD")) if "PD_THRESHOLD" in dbutils.widgets.getArgumentNames() else 0.25

approved = scores.filter(F.col("pd") <= threshold)
declined = scores.filter(F.col("pd") > threshold)

display(approved.limit(10))
display(declined.limit(10))

# Reason codes placeholder (attach SHAP in production)
from pyspark.sql.functions import lit
approved = approved.withColumn("reason_codes", lit("LOW_PD"))
declined = declined.withColumn("reason_codes", lit("HIGH_PD"))

# Adverse action draft (template)
def adverse_action_row(merchant_id, reasons):
    top = "\n".join([f"- {r}" for r in reasons.split(",")[:4]])
    return f"Based on our evaluation, factors include:\n{top}\nContact support@example.com for details."

from pyspark.sql.types import StringType
spark.udf.register("adverse_action_udf", adverse_action_row, StringType())

declined = declined.withColumn("adverse_action_letter", F.expr("adverse_action_udf(merchant_id, reason_codes)"))
declined.write.mode("overwrite").saveAsTable("temp__decline_letters")

# Dashboard-friendly aggregates
spark.sql(f"""
CREATE OR REPLACE TEMP VIEW v_credit_metrics AS
SELECT
  COUNT(*) AS total, SUM(CASE WHEN pd <= {threshold} THEN 1 END) AS approved,
  SUM(CASE WHEN pd > {threshold} THEN 1 END) AS declined,
  AVG(pd) AS avg_pd
FROM temp__scores_latest
""")

display(spark.table("v_credit_metrics"))
