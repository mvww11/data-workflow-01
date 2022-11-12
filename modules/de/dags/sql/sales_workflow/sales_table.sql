create table if not exists sales (
    idx int,
    value float,
    date date,
    store_idx int
);
COPY sales(idx, value, date, store_idx)
FROM '/var/tmp/sales-{{ ds }}.csv' DELIMITER ',' CSV HEADER;