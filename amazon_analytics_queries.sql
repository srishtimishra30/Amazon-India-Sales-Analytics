-- AMAZON FASHION ANALYTICS - MySQL Queries
USE amazon_fashion;

-- Query 1: Business KPIs
SELECT COUNT(*) AS total_orders,
    ROUND(SUM(CASE WHEN is_cancelled=0 THEN amount END),2) AS total_revenue,
    ROUND(AVG(CASE WHEN is_cancelled=0 THEN amount END),2) AS avg_order_value,
    SUM(is_cancelled) AS cancellations,
    ROUND(SUM(is_cancelled)*100.0/COUNT(*),2) AS cancel_rate_pct
FROM orders;

-- Query 2: Monthly Revenue
SELECT order_month, COUNT(*) AS orders,
    ROUND(SUM(CASE WHEN is_cancelled=0 THEN amount END),2) AS revenue
FROM orders GROUP BY order_month ORDER BY order_month;

-- Query 3: Revenue by Category
SELECT category, COUNT(*) AS orders,
    ROUND(SUM(CASE WHEN is_cancelled=0 THEN amount END),2) AS revenue,
    ROUND(SUM(is_cancelled)*100.0/COUNT(*),2) AS cancel_rate
FROM orders GROUP BY category ORDER BY revenue DESC;

-- Query 4: Top States
SELECT ship_state, COUNT(*) AS orders,
    ROUND(SUM(CASE WHEN is_cancelled=0 THEN amount END),2) AS revenue
FROM orders GROUP BY ship_state ORDER BY revenue DESC LIMIT 10;

-- Query 5: Fulfilment Analysis
SELECT fulfilment, COUNT(*) AS orders,
    ROUND(SUM(is_cancelled)*100.0/COUNT(*),2) AS cancel_rate
FROM orders GROUP BY fulfilment;

-- Query 6: B2B vs B2C
SELECT CASE WHEN is_b2b=1 THEN 'B2B' ELSE 'B2C' END AS type,
    COUNT(*) AS orders,
    ROUND(AVG(amount),2) AS avg_order_value
FROM orders GROUP BY is_b2b;

-- Query 7: Cancellation by State+Category
SELECT ship_state, category, COUNT(*) AS orders,
    ROUND(SUM(is_cancelled)*100.0/COUNT(*),2) AS cancel_rate
FROM orders WHERE ship_state IS NOT NULL
GROUP BY ship_state, category
HAVING orders > 100 ORDER BY cancel_rate DESC LIMIT 20;

-- Query 8: Top SKUs
SELECT sku, category, SUM(qty) AS units_sold,
    ROUND(SUM(CASE WHEN is_cancelled=0 THEN amount END),2) AS revenue
FROM orders WHERE is_cancelled=0
GROUP BY sku, category ORDER BY units_sold DESC LIMIT 15;

-- Query 9: Size Distribution
SELECT category, size, COUNT(*) AS orders
FROM orders WHERE is_cancelled=0
GROUP BY category, size ORDER BY category, orders DESC;

-- Query 10: Service Level Impact
SELECT service_level, COUNT(*) AS orders,
    ROUND(SUM(is_cancelled)*100.0/COUNT(*),2) AS cancel_rate
FROM orders GROUP BY service_level;