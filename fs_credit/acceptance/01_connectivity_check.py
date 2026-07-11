# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC ### Connectivity & Tables Exist

spark.sql("SELECT 1").show()
spark.sql("SHOW TABLES").show()
