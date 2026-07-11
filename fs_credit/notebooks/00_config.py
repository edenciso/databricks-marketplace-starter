# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # fs_credit — Config

CATALOG = dbutils.widgets.get("CATALOG") if "CATALOG" in dbutils.widgets.getArgumentNames() else "catalog"
SCHEMA = "fs_credit"
