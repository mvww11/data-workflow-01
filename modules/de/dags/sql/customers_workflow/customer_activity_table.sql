drop table if exists customer_activity;
create table if not exists customer_activity (
    idx int,
    valid_from date,
    valid_to date,
    scd_a float,
    scd_b int
);
COPY customer_activity(idx, valid_from, valid_to, scd_a, scd_b)
FROM {{ params.path }} DELIMITER ',' CSV HEADER;