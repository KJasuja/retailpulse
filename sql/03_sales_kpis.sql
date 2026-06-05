-- 03_sales_kpis.sql
-- Revenue trends, growth, and top products / markets.

-- Monthly revenue with month-over-month growth
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', invoice_date) AS month,
        ROUND(SUM(revenue), 2)            AS revenue,
        COUNT(DISTINCT invoice)           AS orders,
        COUNT(DISTINCT customer_id)       AS customers
    FROM transactions
    GROUP BY 1
)
SELECT
    month,
    revenue,
    orders,
    customers,
    ROUND(revenue / NULLIF(orders, 0), 2) AS avg_order_value,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- Top 10 products by revenue
SELECT
    stock_code,
    ANY_VALUE(description)     AS description,
    ROUND(SUM(revenue), 2)     AS revenue,
    SUM(quantity)              AS units_sold
FROM transactions
GROUP BY stock_code
ORDER BY revenue DESC
LIMIT 10;

-- Revenue by country (top markets)
SELECT
    country,
    ROUND(SUM(revenue), 2)        AS revenue,
    COUNT(DISTINCT customer_id)   AS customers
FROM transactions
GROUP BY country
ORDER BY revenue DESC
LIMIT 15;
