-- 02_retention_kpis.sql
-- Cohort retention: group customers by the month of their first purchase,
-- then measure how many remain active in later months.

WITH first_purchase AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(invoice_date)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
),
activity AS (
    SELECT
        t.customer_id,
        fp.cohort_month,
        DATE_TRUNC('month', t.invoice_date) AS active_month
    FROM transactions t
    JOIN first_purchase fp USING (customer_id)
    GROUP BY t.customer_id, fp.cohort_month, DATE_TRUNC('month', t.invoice_date)
)
SELECT
    cohort_month,
    DATEDIFF('month', cohort_month, active_month) AS month_offset,
    COUNT(DISTINCT customer_id)                   AS active_customers
FROM activity
GROUP BY cohort_month, month_offset
ORDER BY cohort_month, month_offset;

-- Overall repeat-purchase rate (a simple churn proxy)
SELECT
    ROUND(100.0 * SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN orders = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS one_and_done_pct
FROM (
    SELECT customer_id, COUNT(DISTINCT invoice) AS orders
    FROM transactions
    GROUP BY customer_id
) c;
