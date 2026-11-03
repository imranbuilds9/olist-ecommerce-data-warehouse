
import csv
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "olist_order_reviews_dataset.csv"

counts = Counter()
examples = defaultdict(list)

with open(DATA_FILE, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        review_id = row["review_id"]
        counts[review_id] += 1

        if len(examples[review_id]) < 5:
            examples[review_id].append(
                (
                    row["order_id"],
                    row["review_score"],
                    row["review_creation_date"],
                    row["review_answer_timestamp"],
                )
            )

duplicates = {
    review_id: count
    for review_id, count in counts.items()
    if count > 1
}

print("Repeated review IDs:", len(duplicates))
print(
    "Rows belonging to repeated IDs:",
    sum(duplicates.values()),
)

for review_id, count in list(duplicates.items())[:5]:
    print(f"\nReview ID: {review_id} | Occurrences: {count}")

    for example in examples[review_id]:
        print("  ", example)
