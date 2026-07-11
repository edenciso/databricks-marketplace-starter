# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Load Synthetic Samples — fs_credit

# COMMAND ----------
from pyspark.sql import functions as F
from datetime import date, timedelta
import random

catalog = "catalog"; schema = "fs_credit"
spark.sql(f"USE CATALOG {catalog}"); spark.sql(f"USE SCHEMA {schema}")

# Generate 30 days synthetic data
days = 30
merchants = [f"m_{i:05d}" for i in range(300)]
regions = ["NE","SE","MW","SW","W"]
mccs = ["5411","5732","5812","5999"]

rows = []
base = date.today() - timedelta(days=days)
for d in range(days):
    dt = base + timedelta(days=d)
    for m in merchants:
        rows.append((dt, m, random.choice(mccs), random.choice(regions),
                     random.randint(5,80), random.uniform(500,10000),
                     random.uniform(400,9000), random.uniform(10,200),
                     random.randint(0,2), random.randint(0,1),
                     random.uniform(0.0,0.2), random.randint(30,3000),
                     (dt.weekday()+1), dt.day, random.choice([True,False,False])))

df = spark.createDataFrame(rows, """
 dt DATE, merchant_id STRING, mcc STRING, region STRING, tx_count BIGINT, gross_volume DOUBLE, net_volume DOUBLE,
 avg_ticket DOUBLE, refunds_count BIGINT, chargebacks_count BIGINT, auth_decline_rate DOUBLE, tenure_days INT,
 dow INT, dom INT, holiday_flag BOOLEAN
""")
df.write.mode("overwrite").saveAsTable("features__merchant_daily_cashflow")

# Minimal other tables
spark.createDataFrame([(base + timedelta(days=i), m, random.randint(0,1), random.uniform(0,5000), random.uniform(0.3,0.9))
                       for i in range(days) for m in merchants],
                      "dt DATE, merchant_id STRING, cb_count BIGINT, cb_amt DOUBLE, cb_win_rate DOUBLE"
).write.mode("overwrite").saveAsTable("features__events_chargeback")

spark.createDataFrame([(base + timedelta(days=i), m, random.choice([True,False]), random.randint(0,3),
                        random.randint(1,5), random.uniform(0,0.3))
                       for i in range(days) for m in merchants],
                      "dt DATE, merchant_id STRING, risk_flag BOOLEAN, velocity_alerts INT, device_fingerprint_count INT, ip_geo_mismatch_rate DOUBLE"
).write.mode("overwrite").saveAsTable("features__acquirer_features")

spark.createDataFrame([(m, random.choice(["<1yr","1-3yr",">3yr"]), random.choice(["1-9","10-49","50-199","200+"]),
                        random.choice(["<250k","250k-1m","1m-5m","5m+"]), random.choice(["Retail","Food","Services"]))
                       for m in merchants],
                      "merchant_id STRING, entity_age_bucket STRING, employees_bucket STRING, est_revenue_bucket STRING, industry_bucket STRING"
).write.mode("overwrite").saveAsTable("features__firmographics")

spark.createDataFrame([(base + timedelta(days=i), r, random.uniform(3,9), random.uniform(80,120), random.uniform(-1,1))
                       for i in range(days) for r in regions],
                      "dt DATE, region STRING, unemployment_rate DOUBLE, retail_index DOUBLE, smallbiz_sentiment DOUBLE"
).write.mode("overwrite").saveAsTable("features__macro_signals")

display(spark.sql("SHOW TABLES"))
