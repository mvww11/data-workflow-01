DROP TABLE if EXISTS store_locations;
CREATE TABLE if NOT EXISTS store_locations (idx INT, location VARCHAR(50));
copy store_locations(idx, location)
FROM {{ params.path }} delimiter ',' csv header;