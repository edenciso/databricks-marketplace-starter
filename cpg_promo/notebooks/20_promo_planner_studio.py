# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Studio — Promo Planner (cpg_promo)

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window

catalog="catalog"; schema="cpg_promo"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

uplift = spark.table("temp__promo_uplift_latest")
inv = spark.table("features__inventory_position").alias("i")
today = spark.sql("SELECT max(dt) AS dt FROM features__sales_store_sku_day").first()["dt"]

# Join simple inventory snapshot
cand = (uplift.alias("u")
        .join(inv, (F.col("u.store_id")==F.col("i.store_id")) & (F.col("u.sku_id")==F.col("i.sku_id")) & (F.col("i.dt")==today), "left")
        .withColumn("stock_risk", F.when(F.col("on_hand") < 20, F.lit("HIGH")).otherwise(F.lit("OK"))))

# Rank by uplift_revenue with stock guardrail
plan = (cand
        .withColumn("rank", F.row_number().over(Window.partitionBy("store_id").orderBy(F.desc("uplift_revenue"))))
        .filter("rank <= 10")
        .orderBy(F.desc("uplift_revenue")))

display(plan.limit(25))

# Creative generation/scoring placeholder
from pyspark.sql.functions import lit
plan = plan.withColumn("creative_variant", lit("Variant A")).withColumn("predicted_lift_pct", lit(0.12))
plan.write.mode("overwrite").saveAsTable("temp__promo_plan_latest")
