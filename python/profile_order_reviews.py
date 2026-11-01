import csv
from collections import Counter

path = r"data\raw\olist_order_reviews_dataset.csv"

total_rows = 0

review_ids = []
order_ids = []
scores = Counter()

missing = Counter()
invalid_scores = 0
blank_titles = 0
blank_messages = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    print("Columns:", reader.fieldnames)

    for row in reader:
        total_rows += 1

        review_id = row["review_id"].strip()
        order_id = row["order_id"].strip()
        score = row["review_score"].strip()

        review_ids.append(review_id)
        order_ids.append(order_id)

        if not review_id:
            missing["review_id"] += 1

        if not order_id:
            missing["order_id"] += 1

        if not score:
            missing["review_score"] += 1
        elif score not in {"1", "2", "3", "4", "5"}:
            invalid_scores += 1
        else:
            scores[score] += 1

        if not row["review_comment_title"].strip():
            blank_titles += 1

        if not row["review_comment_message"].strip():
            blank_messages += 1

        if not row["review_creation_date"].strip():
            missing["review_creation_date"] += 1

        if not row["review_answer_timestamp"].strip():
            missing["review_answer_timestamp"] += 1


review_id_counts = Counter(review_ids)
order_id_counts = Counter(order_ids)

duplicate_review_ids = {
    key: count for key, count in review_id_counts.items()
    if key and count > 1
}

duplicate_order_ids = {
    key: count for key, count in order_id_counts.items()
    if key and count > 1
}

print("\n" + "=" * 55)
print("ORDER REVIEWS PROFILE")
print("=" * 55)

print("Total rows:", total_rows)

print("\n--- ID PROFILE ---")
print("Distinct review IDs:", len(set(review_ids)))
print("Distinct order IDs:", len(set(order_ids)))
print("Missing values:", dict(missing))

print("Duplicate review_id groups:", len(duplicate_review_ids))
print("Rows involved in duplicate review_id groups:",
      sum(duplicate_review_ids.values()))

print("Duplicate order_id groups:", len(duplicate_order_ids))
print("Rows involved in duplicate order_id groups:",
      sum(duplicate_order_ids.values()))

print("\n--- SCORE PROFILE ---")
print("Score distribution:", dict(sorted(scores.items())))
print("Invalid scores:", invalid_scores)

print("\n--- COMMENT PROFILE ---")
print("Blank review titles:", blank_titles)
print("Blank review messages:", blank_messages)

print("\n--- TIMESTAMP PROFILE ---")
print("Missing creation dates:", missing["review_creation_date"])
print("Missing answer timestamps:", missing["review_answer_timestamp"])