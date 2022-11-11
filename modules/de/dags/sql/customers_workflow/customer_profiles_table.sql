drop table if exists customer_profiles;

create table if not exists customer_profiles (
    idx int,
    attr_a int,
    attr_b char(1),
    attr_c varchar(3)
);

COPY customer_profiles(idx, attr_a, attr_b, attr_c)
FROM
    {{ params.path }} DELIMITER ',' CSV HEADER;