# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC ### Schema checksum (cpg_promo)

tables = ["features__sales_store_sku_day","features__price_history","features__inventory_position",
          "features__events_calendar","features__weather_dma","features__creatives_meta"]
for t in tables:
    df = spark.table(t).limit(1)
    print(t, sorted([f.name+':'+f.dataType.simpleString() for f in df.schema.fields]))
