---                                        ** INSPECTING TABLES **

-- checking table names and no. of columns
SELECT
    table_name,
    COUNT(*) AS column_count
FROM information_schema.columns
WHERE table_schema = 'raw'
GROUP BY table_name
ORDER BY table_name;

SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'raw'
ORDER BY table_name, ordinal_position;

SELECT
    datname AS database_name,
    datcollate AS collation,
    datctype AS character_classification
FROM pg_database
WHERE datname = current_database();


-- counting rows of all tables
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM raw.customers

UNION ALL

SELECT 'geolocation', COUNT(*) FROM raw.geolocation

UNION ALL

SELECT 'orders', COUNT(*) FROM raw.orders

UNION ALL

SELECT 'order_items', COUNT(*) FROM raw.order_items

UNION ALL

SELECT 'order_payments', COUNT(*) FROM raw.order_payments

UNION ALL

SELECT 'order_reviews', COUNT(*) FROM raw.order_reviews

UNION ALL

SELECT 'products', COUNT(*) FROM raw.products

UNION ALL

SELECT 'sellers', COUNT(*) FROM raw.sellers

UNION ALL

SELECT 'product_category_translation', COUNT(*)
FROM raw.product_category_translation

ORDER BY table_name;


-- checking if the metadata is correctly populated
SELECT
    'customers' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT batch_id) AS batch_count,
    COUNT(DISTINCT source_file) AS source_file_count,
    COUNT(*) FILTER (
        WHERE batch_id IS NULL
           OR source_file IS NULL
           OR ingested_at IS NULL
    ) AS missing_metadata
FROM raw.customers

UNION ALL

SELECT
    'geolocation', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.geolocation

UNION ALL

SELECT
    'orders', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.orders

UNION ALL

SELECT
    'order_items', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.order_items

UNION ALL

SELECT
    'order_payments', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.order_payments

UNION ALL

SELECT
    'order_reviews', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.order_reviews

UNION ALL

SELECT
    'products', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.products

UNION ALL

SELECT
    'sellers', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.sellers

UNION ALL

SELECT
    'product_category_translation', COUNT(*), COUNT(DISTINCT batch_id),
    COUNT(DISTINCT source_file),
    COUNT(*) FILTER (WHERE batch_id IS NULL OR source_file IS NULL OR ingested_at IS NULL)
FROM raw.product_category_translation

ORDER BY table_name;


-- checking ingestion timestamp
SELECT
    batch_id,
    MIN(ingested_at) AS earliest_ingestion,
    MAX(ingested_at) AS latest_ingestion,
    COUNT(DISTINCT ingested_at) AS distinct_timestamps,
    COUNT(*) AS total_rows
FROM (
    SELECT batch_id, ingested_at FROM raw.customers
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.geolocation
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.orders
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.order_items
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.order_payments
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.order_reviews
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.products
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.sellers
    UNION ALL
    SELECT batch_id, ingested_at FROM raw.product_category_translation
) AS all_raw_data
GROUP BY batch_id;


-- checking source file
SELECT 'customers' AS table_name,
       source_file,
       COUNT(*) AS row_count
FROM raw.customers
GROUP BY source_file

UNION ALL

SELECT 'geolocation', source_file, COUNT(*)
FROM raw.geolocation
GROUP BY source_file

UNION ALL

SELECT 'orders', source_file, COUNT(*)
FROM raw.orders
GROUP BY source_file

UNION ALL

SELECT 'order_items', source_file, COUNT(*)
FROM raw.order_items
GROUP BY source_file

UNION ALL

SELECT 'order_payments', source_file, COUNT(*)
FROM raw.order_payments
GROUP BY source_file

UNION ALL

SELECT 'order_reviews', source_file, COUNT(*)
FROM raw.order_reviews
GROUP BY source_file

UNION ALL

SELECT 'products', source_file, COUNT(*)
FROM raw.products
GROUP BY source_file

UNION ALL

SELECT 'sellers', source_file, COUNT(*)
FROM raw.sellers
GROUP BY source_file

UNION ALL

SELECT 'product_category_translation', source_file, COUNT(*)
FROM raw.product_category_translation
GROUP BY source_file

ORDER BY table_name;


-- checking how the nulls were handled
SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE review_comment_title = ''
    ) AS empty_string_titles,

    COUNT(*) FILTER (
        WHERE review_comment_title IS NULL
    ) AS null_titles,

    COUNT(*) FILTER (
        WHERE review_comment_message = ''
    ) AS empty_string_messages,

    COUNT(*) FILTER (
        WHERE review_comment_message IS NULL
    ) AS null_messages

FROM raw.order_reviews;


-- size of the database after data ingestion
SELECT
    pg_size_pretty(pg_database_size('olist_dw'))
        AS database_size,

    pg_size_pretty(
        pg_total_relation_size('raw.customers')
    ) AS customers_size,

    pg_size_pretty(
        pg_total_relation_size('raw.geolocation')
    ) AS geolocation_size,

    pg_size_pretty(
        pg_total_relation_size('raw.orders')
    ) AS orders_size,

    pg_size_pretty(
        pg_total_relation_size('raw.order_items')
    ) AS order_items_size;
