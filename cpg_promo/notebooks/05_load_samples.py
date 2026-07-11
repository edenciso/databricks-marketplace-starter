# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Load Synthetic Samples — cpg_promo

# COMMAND ----------
from pyspark.sql import functions as F
from datetime import date, timedelta
import random

catalog="catalog"; schema="cpg_promo"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

days = 28
stores = [f"s{i:03d}" for i in range(50)]
skus = [f"sku{i:04d}" for i in range(200)]
cats = ["beverage","snacks","personal_care","dairy"]
dmas = ["001","003","005","007","009"]

base = date.today() - timedelta(days=days)

# sales
rows = []
for i in range(days):
    dt = base + timedelta(days=i)
    for s in stores:
        for sku in random.sample(skus, 60):
            rows.append((dt, s, sku, random.choice(cats),
                         random.randint(0,80), random.uniform(0,800),
                         random.randint(0,3), random.uniform(1,15),
                         random.choice([True,False,False]), random.choice([True,False,False,False])))
spark.createDataFrame(rows, """
 dt DATE, store_id STRING, sku_id STRING, category STRING, units_sold BIGINT, gross_sales DOUBLE, returns_units BIGINT,
 price_paid DOUBLE, promo_flag BOOLEAN, stockout_flag BOOLEAN
""").write.mode("overwrite").saveAsTable("features__sales_store_sku_day")

# price history
spark.sql("""
CREATE OR REPLACE TABLE features__price_history AS
SELECT dt, store_id, sku_id,
       ROUND(price_paid * (1.0 + rand()*0.1),2) AS list_price,
       CASE WHEN promo_flag THEN ROUND(price_paid*0.85,2) ELSE price_paid END AS promo_price,
       CASE WHEN price_paid < 3 THEN 'low' WHEN price_paid < 7 THEN 'mid' ELSE 'high' END AS price_bucket
FROM features__sales_store_sku_day
""")

# inventory
spark.createDataFrame([
    (base + timedelta(days=i), s, sku, random.randint(0,300), random.randint(0,200), random.randint(1,14))
    for i in range(days) for s in stores for sku in random.sample(skus, 40)
], "dt DATE, store_id STRING, sku_id STRING, on_hand INT, on_order INT, lead_time_days INT"
).write.mode("overwrite").saveAsTable("features__inventory_position")

# events & weather
spark.createDataFrame([(base + timedelta(days=i), random.choice(dmas), random.choice(["holiday","sports","concert"]), random.uniform(0,1))
                       for i in range(days) for _ in range(5)],
                      "event_date DATE, dma STRING, event_type STRING, intensity DOUBLE"
).write.mode("overwrite").saveAsTable("features__events_calendar")

spark.createDataFrame([(base + timedelta(days=i), d, random.uniform(0,35), random.uniform(0,50), random.choice([True,False,False]))
                       for i in range(days) for d in dmas],
                      "dt DATE, dma STRING, temp DOUBLE, precip DOUBLE, extreme_flag BOOLEAN"
).write.mode("overwrite").saveAsTable("features__weather_dma")

# creatives meta (toy)
spark.createDataFrame([
    (f"c{i:04d}", random.choice(["BrandA","BrandB"]), random.choice(["display","video"]),
     random.choice([6,15,30]), random.randint(20,120), [random.random() for _ in range(8)],
     random.uniform(0.005,0.08), random.uniform(1.0,8.0))
    for i in range(120)
], "creative_id STRING, brand STRING, format STRING, duration_sec INT, text_len INT, palette_embedding ARRAY<DOUBLE>, historic_ctr DOUBLE, historic_dwell DOUBLE"
).write.mode("overwrite").saveAsTable("features__creatives_meta")

display(spark.sql("SHOW TABLES"))
