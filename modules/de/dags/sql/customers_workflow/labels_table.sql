drop table if exists labels;

create table if not exists labels (
    idx int,
    label int
);

COPY labels(idx, label)
FROM
    {{ params.path }} DELIMITER ',' CSV HEADER;