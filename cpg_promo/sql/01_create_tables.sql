-- Adjust the catalog name as needed
USE CATALOG catalog;
CREATE SCHEMA IF NOT EXISTS cpg_promo;
USE SCHEMA cpg_promo;

CREATE TABLE IF NOT EXISTS features__sales_store_sku_day (
  dt DATE,
  store_id STRING,
  sku_id STRING,
  category STRING,
  units_sold BIGINT,
  gross_sales DOUBLE,
  returns_units BIGINT,
  price_paid DOUBLE,
  promo_flag BOOLEAN,
  stockout_flag BOOLEAN
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__price_history (
  dt DATE,
  store_id STRING,
  sku_id STRING,
  list_price DOUBLE,
  promo_price DOUBLE,
  price_bucket STRING
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__promo_calendar (
  promo_id STRING,
  sku_id STRING,
  store_id STRING,
  start_date DATE,
  end_date DATE,
  mechanic STRING,
  ad_channel STRING
);

CREATE TABLE IF NOT EXISTS features__inventory_position (
  dt DATE,
  store_id STRING,
  sku_id STRING,
  on_hand INT,
  on_order INT,
  lead_time_days INT
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__events_calendar (
  event_date DATE,
  dma STRING,
  event_type STRING,
  intensity DOUBLE
);

CREATE TABLE IF NOT EXISTS features__weather_dma (
  dt DATE,
  dma STRING,
  temp DOUBLE,
  precip DOUBLE,
  extreme_flag BOOLEAN
)
PARTITIONED BY (dt);

CREATE TABLE IF NOT EXISTS features__creatives_meta (
  creative_id STRING,
  brand STRING,
  format STRING,
  duration_sec INT,
  text_len INT,
  palette_embedding ARRAY<DOUBLE>,
  historic_ctr DOUBLE,
  historic_dwell DOUBLE
);
