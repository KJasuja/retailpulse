-- 04_marketing_kpis.sql
-- RFM (Recency, Frequency, Monetary) scoring, value tiers, and an LTV proxy.

WITH snapshot AS (
    SELECT MAX(invoice_date) + INTERVAL 1 DAY AS as_of FROM transactions
),
rfm AS (
    SELECT
        t.customer_id,
        DATEDIFF('day', MAX(t.invoice_date), s.as_of) AS recency_days,
        COUNT(DISTINCT t.invoice)                     AS frequency,
        ROUND(SUM(t.revenue), 2)                      AS monetary
    FROM transactions t
    CROSS JOIN snapshot s
    GROUP BY t.customer_id, s.as_of
),
scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,  -- recent = high
        NTILE(5) OVER (ORDER BY frequency)         AS f_score,
        NTILE(5) OVER (ORDER BY monetary)          AS m_score
    FROM rfm
)
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score, f_score, m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN f_score >= 4                  THEN 'Loyal'
        WHEN r_score >= 4                  THEN 'New / Promising'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'At Risk'
        ELSE 'Needs Attention'
    END AS segment
FROM scored
ORDER BY rfm_total DESC;

-- Value-tier summary: who drives the revenue?
WITH ranked AS (
    SELECT customer_id, SUM(revenue) AS ltv,
           NTILE(10) OVER (ORDER BY SUM(revenue) DESC) AS decile
    FROM transactions GROUP BY customer_id
)
SELECT
    decile,
    COUNT(*)                                   AS customers,
    ROUND(SUM(ltv), 2)                         AS revenue,
    ROUND(100.0 * SUM(ltv) / SUM(SUM(ltv)) OVER (), 1) AS pct_of_revenue
FROM ranked
GROUP BY decile
ORDER BY decile;
