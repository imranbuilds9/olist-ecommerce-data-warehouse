--                                            **Creating tables**
-- 1. Customers
CREATE TABLE raw.customers (
    customer_id TEXT,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 2. Geolocation
CREATE TABLE raw.geolocation (
    geolocation_zip_code_prefix TEXT,
    geolocation_lat TEXT,
    geolocation_lng TEXT,
    geolocation_city TEXT,
    geolocation_state TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 3. Orders
CREATE TABLE raw.orders (
    order_id TEXT,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 4. Order items
CREATE TABLE raw.order_items (
    order_id TEXT,
    order_item_id TEXT,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    price TEXT,
    freight_value TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 5. Order payments
CREATE TABLE raw.order_payments (
    order_id TEXT,
    payment_sequential TEXT,
    payment_type TEXT,
    payment_installments TEXT,
    payment_value TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 6. Order reviews
CREATE TABLE raw.order_reviews (
    review_id TEXT,
    order_id TEXT,
    review_score TEXT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 7. Products
CREATE TABLE raw.products (
    product_id TEXT,
    product_category_name TEXT,
    product_name_lenght TEXT,
    product_description_lenght TEXT,
    product_photos_qty TEXT,
    product_weight_g TEXT,
    product_length_cm TEXT,
    product_height_cm TEXT,
    product_width_cm TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 8. Sellers
CREATE TABLE raw.sellers (
    seller_id TEXT,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);

-- 9. Product category translation
CREATE TABLE raw.product_category_translation (
    product_category_name TEXT,
    product_category_name_english TEXT,
    source_file TEXT NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL,
    batch_id UUID NOT NULL
);
