-- Generating sql queries that check for the null values in each column of all 9 tables
SELECT
    table_name,
    column_name,
    'SELECT '
    || quote_literal(table_name) || ' AS table_name, '
    || quote_literal(column_name) || ' AS column_name, '
    || 'COUNT(*) FILTER (WHERE '
    || quote_ident(column_name)
    || ' IS NULL) AS null_count '
    || 'FROM raw.'
    || quote_ident(table_name)
    || ';' AS generated_sql
FROM information_schema.columns
WHERE table_schema = 'raw'
  AND column_name NOT IN (
      'source_file',
      'ingested_at',
      'batch_id'
  )
ORDER BY table_name, ordinal_position;


-- running the above generated queries using a 'DO' block to investigate null values
CREATE TEMP TABLE null_check_results (
    table_name TEXT,
    column_name TEXT,
    null_count BIGINT
);

DO $$
DECLARE
    col RECORD;
    sql_query TEXT;
BEGIN
    FOR col IN
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'raw'
          AND column_name NOT IN (
              'source_file',
              'ingested_at',
              'batch_id'
          )
        ORDER BY table_name, ordinal_position
    LOOP
        sql_query := format(
            'INSERT INTO null_check_results
             SELECT %L, %L, COUNT(*)
             FILTER (WHERE %I IS NULL)
             FROM raw.%I',
            col.table_name,
            col.column_name,
            col.column_name,
            col.table_name
        );

        EXECUTE sql_query;
    END LOOP;
END $$;

SELECT *
FROM null_check_results
ORDER BY table_name, column_name;


-- investigating empty string values '' using the same above method

CREATE TEMP TABLE empty_string_results (
    table_name TEXT,
    column_name TEXT,
    empty_count BIGINT
);

DO $$
DECLARE
    col RECORD;
    sql_query TEXT;
BEGIN
    FOR col IN
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'raw'
          AND column_name NOT IN (
              'source_file',
              'ingested_at',
              'batch_id'
          )
        ORDER BY table_name, ordinal_position
    LOOP
        sql_query := format(
            'INSERT INTO empty_string_results
             SELECT %L, %L, COUNT(*)
             FILTER (WHERE %I = %L)
             FROM raw.%I',
            col.table_name,
            col.column_name,
            col.column_name,
            '',
            col.table_name
        );

        EXECUTE sql_query;
    END LOOP;
END $$;

SELECT *
FROM empty_string_results
WHERE empty_count > 0
ORDER BY table_name, column_name;


-- investigating if the four missing product dimensions and attributes belong to the same product rows
SELECT
    COUNT(*) AS total_products,

    COUNT(*) FILTER (
        WHERE product_category_name = ''
    ) AS missing_category,

    COUNT(*) FILTER (
        WHERE product_description_lenght = ''
    ) AS missing_description_length,

    COUNT(*) FILTER (
        WHERE product_name_lenght = ''
    ) AS missing_name_length,

    COUNT(*) FILTER (
        WHERE product_photos_qty = ''
    ) AS missing_photo_count,

    COUNT(*) FILTER (
        WHERE product_weight_g = ''
          AND product_length_cm = ''
          AND product_height_cm = ''
          AND product_width_cm = ''
    ) AS missing_all_four_dimensions,

    COUNT(*) FILTER (
        WHERE product_category_name = ''
          AND product_description_lenght = ''
          AND product_name_lenght = ''
          AND product_photos_qty = ''
    ) AS missing_all_four_attributes
FROM raw.products;

-- Inspecting two products with missing dimensions
SELECT
    product_id,
    product_category_name,
    product_name_lenght,
    product_description_lenght,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM raw.products
WHERE product_weight_g = ''
  AND product_length_cm = ''
  AND product_height_cm = ''
  AND product_width_cm = '';

-- Verifying empty order timestamps against order status
SELECT
    order_status,
    COUNT(*) AS total_orders,

    COUNT(*) FILTER (
        WHERE order_approved_at = ''
    ) AS missing_approval_timestamp,

    COUNT(*) FILTER (
        WHERE order_delivered_carrier_date = ''
    ) AS missing_carrier_timestamp,

    COUNT(*) FILTER (
        WHERE order_delivered_customer_date = ''
    ) AS missing_customer_delivery_timestamp

FROM raw.orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- inspecting delivered orders with missing timestamps
SELECT
    order_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date
FROM raw.orders
WHERE order_status = 'delivered'
  AND (
      order_approved_at = ''
      OR order_delivered_carrier_date = ''
      OR order_delivered_customer_date = ''
  )
ORDER BY order_purchase_timestamp;
