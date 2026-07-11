-- Provider-side Delta Sharing templates (adjust names/paths)
USE CATALOG catalog;
CREATE SHARE IF NOT EXISTS cpg_promo_share;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__sales_store_sku_day;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__price_history;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__promo_calendar;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__inventory_position;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__events_calendar;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__weather_dma;
ALTER SHARE cpg_promo_share ADD TABLE catalog.cpg_promo.features__creatives_meta;
