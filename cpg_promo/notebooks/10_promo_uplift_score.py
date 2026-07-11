# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Pro — Promo Uplift Scoring (cpg_promo)

# COMMAND ----------
import numpy as np, pandas as pd, mlflow
from pyspark.sql import functions as F

catalog="catalog"; schema="cpg_promo"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

base = spark.table("features__sales_store_sku_day")   .join(spark.table("features__price_history"), ["dt","store_id","sku_id"], "left")   .join(spark.table("features__inventory_position"), ["dt","store_id","sku_id"], "left")

# Events/weather joins (toy DMA mapping: first 3 of store_id)
events = spark.table("features__events_calendar")
weather = spark.table("features__weather_dma")
df = (base.join(events, (base.dt==events.event_date) & (base.store_id.substr(2,3)==events.dma), "left")
          .join(weather, (base.dt==weather.dt) & (base.store_id.substr(2,3)==weather.dma), "left"))

scoring_day = spark.sql("SELECT max(dt) AS dt FROM features__sales_store_sku_day").first()["dt"]
pdf = df.filter(F.col("dt")==scoring_day).toPandas()

# Placeholder uplift: random but higher when promo_flag
uplift = (0.05 + 0.15*pdf["promo_flag"].astype(int) + 0.05*np.random.rand(len(pdf))).clip(0,0.5)
out = pd.DataFrame({
    "store_id": pdf["store_id"],
    "sku_id": pdf["sku_id"],
    "uplift_units": (uplift * (pdf["units_sold"]+1)).round(2),
    "uplift_revenue": (uplift * (pdf["gross_sales"]+1)).round(2)
})
spark.createDataFrame(out).write.mode("overwrite").saveAsTable("temp__promo_uplift_latest")
display(spark.table("temp__promo_uplift_latest").limit(10))
