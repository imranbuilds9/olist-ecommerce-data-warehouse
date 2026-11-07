import csv
import uuid
import getpass
from datetime import datetime, timezone
from pathlib import Path

import psycopg
from psycopg import sql


# Configuration

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "olist_dw",
    "user": "postgres",
}

# Each entry contains:
# CSV filename, PostgreSQL table, original source columns
CSV_TABLES = [
    (
        "olist_customers_dataset.csv",
        "customers",
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ],
    ),
    (
        "olist_geolocation_dataset.csv",
        "geolocation",
        [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state",
        ],
    ),
    (
        "olist_orders_dataset.csv",
        "orders",
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    ),
    (
        "olist_order_items_dataset.csv",
        "order_items",
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ],
    ),
    (
        "olist_order_payments_dataset.csv",
        "order_payments",
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ],
    ),
    (
        "olist_order_reviews_dataset.csv",
        "order_reviews",
        [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp",
        ],
    ),
    (
        "olist_products_dataset.csv",
        "products",
        [
            "product_id",
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
    ),
    (
        "olist_sellers_dataset.csv",
        "sellers",
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ],
    ),
    (
        "product_category_name_translation.csv",
        "product_category_translation",
        [
            "product_category_name",
            "product_category_name_english",
        ],
    ),
]

METADATA_COLUMNS = [
    "source_file",
    "ingested_at",
    "batch_id",
]


# Ingestion

def main():
    batch_id = uuid.uuid4()
    ingested_at = datetime.now(timezone.utc)

    print("Starting Olist raw ingestion")
    print(f"Batch ID: {batch_id}")
    print(f"Ingestion timestamp: {ingested_at.isoformat()}")
    print()

    results = []

    password = getpass.getpass("PostgreSQL password: ")

    # Preflight validation: check all source files before database changes.
    print("Running source file preflight validation...")

    for file_name, _, source_columns in CSV_TABLES:

        file_path = RAW_DATA_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Source file not found: {file_path}"
            )

        with file_path.open(
            mode="r",
            encoding="utf-8-sig",
            newline="",
        ) as csv_file:

            reader = csv.reader(csv_file)
            actual_headers = next(reader, None)

        if actual_headers != source_columns:
            raise ValueError(
                f"Unexpected CSV headers in {file_name}\n"
                f"Expected: {source_columns}\n"
                f"Actual:   {actual_headers}"
            )

        print(f"Validated: {file_name}")

    print("All source files passed preflight validation.")
    print()

    with psycopg.connect(**DB_CONFIG, password=password) as conn:

        # The connection context manages the transaction.
        # Any exception causes the transaction to roll back.

        with conn.cursor() as cur:

            # Full refresh: remove the existing raw snapshot.
            # These DELETE statements are inside the transaction.
            print("Removing previous raw snapshot...")

            for _, table_name, _ in CSV_TABLES:
                cur.execute(
                    sql.SQL("DELETE FROM {}.{}").format(
                        sql.Identifier("raw"),
                        sql.Identifier(table_name),
                    )
                )

            print("Previous snapshot removed within transaction.")
            print()

            # Load each CSV into its corresponding raw table.
            for file_name, table_name, source_columns in CSV_TABLES:

                file_path = RAW_DATA_DIR / file_name

                if not file_path.exists():
                    raise FileNotFoundError(
                        f"Source file not found: {file_path}"
                    )

                copy_columns = source_columns + METADATA_COLUMNS

                copy_statement = sql.SQL(
                    "COPY {}.{} ({}) FROM STDIN"
                ).format(
                    sql.Identifier("raw"),
                    sql.Identifier(table_name),
                    sql.SQL(", ").join(
                        sql.Identifier(column)
                        for column in copy_columns
                    ),
                )

                row_count = 0

                print(f"Loading {file_name}...")

                with file_path.open(
                    mode="r",
                    encoding="utf-8-sig",
                    newline="",
                ) as csv_file:

                    reader = csv.DictReader(csv_file)

                    # Validate CSV headers before loading.
                    if reader.fieldnames != source_columns:
                        raise ValueError(
                            f"Unexpected CSV headers in {file_name}\n"
                            f"Expected: {source_columns}\n"
                            f"Actual:   {reader.fieldnames}"
                        )

                    with cur.copy(copy_statement) as copy:

                        for row in reader:

                            source_values = [
                                row[column]
                                for column in source_columns
                            ]

                            metadata_values = [
                                file_name,
                                ingested_at,
                                batch_id,
                            ]

                            copy.write_row(
                                source_values + metadata_values
                            )

                            row_count += 1

                results.append((table_name, row_count))

                print(
                    f"Loaded {row_count:,} rows "
                    f"into raw.{table_name}"
                )

            # Verify database row counts before committing.
            print()
            print("Verifying loaded row counts...")

            for table_name, expected_count in results:

                cur.execute(
                    sql.SQL(
                        "SELECT COUNT(*) FROM {}.{}"
                    ).format(
                        sql.Identifier("raw"),
                        sql.Identifier(table_name),
                    )
                )

                actual_count = cur.fetchone()[0]

                if actual_count != expected_count:
                    raise RuntimeError(
                        f"Row count mismatch for raw.{table_name}: "
                        f"expected {expected_count}, "
                        f"found {actual_count}"
                    )

                print(
                    f"raw.{table_name}: "
                    f"{actual_count:,} rows verified"
                )

        # The connection context commits after successful completion.
        # If an exception occurs, it rolls back instead.

    print()
    print("RAW INGESTION COMPLETED SUCCESSFULLY")
    print(f"Batch ID: {batch_id}")
    print(f"Total rows loaded: {sum(count for _, count in results):,}")


if __name__ == "__main__":
    main()
