CREATE TABLE if NOT EXISTS monthly_sales (
    store_idx INT,
    location VARCHAR(50),
    sale_month DATE,
    VALUE FLOAT
);
INSERT INTO monthly_sales(
        store_idx,
        location,
        sale_month,
        VALUE
    )
SELECT store_idx,
    location,
    cast(date_trunc('month', date) as date) as sale_month,
    SUM(value)
FROM sales
    left join store_locations on sales.store_idx = store_locations.idx
WHERE CAST(DATE_TRUNC('month', DATE) AS DATE) = '{{ ds }}'
GROUP BY store_idx,
    date_trunc('month', date),
    location