CREATE TABLE if NOT EXISTS feature_store (
    idx INT,
    attr_a int,
    attr_b char(1),
    scd_a float,
    scd_b int,
    label int
);
INSERT INTO feature_store(
        idx,
        attr_a,
        attr_b,
        scd_a,
        scd_b,
        label
    )
SELECT customer_activity.idx,
    attr_a,
    attr_b,
    scd_a,
    scd_b,
    label
FROM customer_activity
    LEFT JOIN customer_profiles ON customer_activity.idx = customer_profiles.idx
    LEFT JOIN labels ON customer_activity.idx = labels.idx
WHERE valid_to IS NULL;