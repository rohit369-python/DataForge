CREATE SCHEMA IF NOT EXISTS analytics;
-- Adapt this view to your deployed fact_sales/dim_date warehouse tables.
CREATE OR REPLACE VIEW analytics.vw_daily_sales AS
SELECT order_date::date AS order_date, COUNT(DISTINCT order_id) AS total_orders, SUM(total_amount) AS total_revenue, SUM(quantity) AS units_sold
FROM fact_sales GROUP BY order_date::date;
