import csv
from collections import defaultdict

path = r"data\raw\olist_order_reviews_dataset.csv"

reviews_by_id = defaultdict(list)
reviews_by_order = defaultdict(list)
exact_rows = defaultdict(int)

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        reviews_by_id[row["review_id"]].append(row)
        reviews_by_order[row["order_id"]].append(row)

        row_signature = tuple(row.values())
        exact_rows[row_signature] += 1


duplicate_review_groups = {
    key: rows for key, rows in reviews_by_id.items()
    if len(rows) > 1
}

duplicate_order_groups = {
    key: rows for key, rows in reviews_by_order.items()
    if len(rows) > 1
}

review_ids_linked_to_multiple_orders = {
    key: rows
    for key, rows in duplicate_review_groups.items()
    if len({row["order_id"] for row in rows}) > 1
}

duplicate_orders_with_multiple_review_ids = {
    key: rows
    for key, rows in duplicate_order_groups.items()
    if len({row["review_id"] for row in rows}) > 1
}

exact_duplicate_groups = {
    signature: count
    for signature, count in exact_rows.items()
    if count > 1
}

print("\n--- DUPLICATE PATTERN SUMMARY ---")

print("Duplicate review_id groups:", len(duplicate_review_groups))
print("Review IDs linked to multiple orders:",
      len(review_ids_linked_to_multiple_orders))

print("Duplicate order_id groups:", len(duplicate_order_groups))
print("Orders linked to multiple review IDs:",
      len(duplicate_orders_with_multiple_review_ids))

print("Exact duplicate full-row groups:", len(exact_duplicate_groups))
print("Rows involved in exact duplicate groups:",
      sum(exact_duplicate_groups.values()))

print("\n--- FIRST 10 DUPLICATE REVIEW IDs ---")

for review_id, rows in list(duplicate_review_groups.items())[:10]:
    print("\nReview ID:", review_id)
    print("Number of rows:", len(rows))
    print("Distinct orders:", len({row["order_id"] for row in rows}))

    for row in rows:
        print(
            "Order:", row["order_id"],
            "| Score:", row["review_score"],
            "| Creation:", row["review_creation_date"],
            "| Answer:", row["review_answer_timestamp"]
        )

print("\n--- FIRST 10 DUPLICATE ORDER IDs ---")

for order_id, rows in list(duplicate_order_groups.items())[:10]:
    print("\nOrder ID:", order_id)
    print("Number of rows:", len(rows))
    print("Distinct review IDs:", len({row["review_id"] for row in rows}))

    for row in rows:
        print(
            "Review ID:", row["review_id"],
            "| Score:", row["review_score"],
            "| Creation:", row["review_creation_date"],
            "| Answer:", row["review_answer_timestamp"]
        )