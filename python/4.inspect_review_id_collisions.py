
import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "olist_order_reviews_dataset.csv"

reviews_by_id = defaultdict(list)

with open(DATA_FILE, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        reviews_by_id[row["review_id"]].append(row)

repeated = {
    review_id: rows
    for review_id, rows in reviews_by_id.items()
    if len(rows) > 1
}

multiple_orders = 0
different_comments = 0
identical_full_rows = 0

for rows in repeated.values():
    if len({row["order_id"] for row in rows}) > 1:
        multiple_orders += 1

    comments = {
        (row["review_comment_title"], row["review_comment_message"])
        for row in rows
    }

    if len(comments) > 1:
        different_comments += 1

    if len({tuple(sorted(row.items())) for row in rows}) == 1:
        identical_full_rows += 1

print("Repeated review ID groups:", len(repeated))
print("Groups linked to multiple orders:", multiple_orders)
print("Groups with different review comments:", different_comments)
print("Groups containing only identical full rows:", identical_full_rows)

print("\nExample with all columns:")
for review_id, rows in repeated.items():
    print("\nReview ID:", review_id)
    for row in rows:
        print(row)
    break
