-- 01_clean_data.sql
-- Build a clean transactions table from the raw Online Retail II data.
-- Dialect: DuckDB / PostgreSQL friendly. Assumes raw data loaded into `raw_transactions`.

-- Expected raw columns:
--   invoice, stock_code, description, quantity, invoice_date, price, customer_id, country

CREATE OR REPLACE TABLE transactions AS
SELECT
    invoice,
    stock_code,
    TRIM(description)              AS description,
    quantity,
    CAST(invoice_date AS TIMESTAMP) AS invoice_date,
    price,
    customer_id,
    country,
    quantity * price              AS revenue
FROM raw_transactions
WHERE customer_id IS NOT NULL          -- drop anonymous rows
  AND quantity > 0                     -- drop returns / cancellations
  AND price    > 0                     -- drop free / adjustment lines
  AND invoice NOT LIKE 'C%';           -- 'C' invoices = cancellations

-- Quick data-quality check
SELECT
    COUNT(*)                              AS rows,
    COUNT(DISTINCT customer_id)           AS customers,
    COUNT(DISTINCT invoice)               AS invoices,
    MIN(invoice_date)                     AS first_order,
    MAX(invoice_date)                     AS last_order,
    ROUND(SUM(revenue), 2)                AS total_revenue
FROM transactions;
