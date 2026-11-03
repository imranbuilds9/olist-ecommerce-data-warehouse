import csv
from datetime import datetime
from collections import Counter

reviews_path = r"data\raw\olist_order_reviews_dataset.csv"
orders_path = r"data\raw\olist_orders_dataset.csv"

orders = {}

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        orders[row["order_id"]] = row

fmt = "%Y-%m-%d %H:%M:%S"

anomalies = []
status_counts = Counter()
day_differences = []

with open(reviews_path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order = orders.get(row["order_id"])

        if not order:
            continue

        review_date = datetime.strptime(
            row["review_creation_date"], fmt
        )

        purchase_date = datetime.strptime(
            order["order_purchase_timestamp"], fmt
        )

        if review_date.date() < purchase_date.date():

            difference = (purchase_date.date() - review_date.date()).days

            status = order["order_status"]

            anomalies.append({
                "order_id": row["order_id"],
                "review_id": row["review_id"],
                "score": row["review_score"],
                "purchase": purchase_date,
                "review_creation": review_date,
                "status": status,
                "difference": difference
            })

            status_counts[status] += 1
            day_differences.append(difference)


print("\nTOTAL ANOMALIES:", len(anomalies))

print("\n--- ORDER STATUS DISTRIBUTION ---")

for status, count in status_counts.items():
    print(status, ":", count)

print("\n--- DATE DIFFERENCE SUMMARY ---")

print("Minimum days:", min(day_differences))
print("Maximum days:", max(day_differences))
print("Average days:", round(sum(day_differences) / len(day_differences), 2))

print("\n--- FIRST 20 ANOMALIES ---")

for item in anomalies[:20]:
    print(
        "\nOrder:", item["order_id"],
        "| Review:", item["review_id"],
        "| Score:", item["score"],
        "| Status:", item["status"],
        "| Purchase:", item["purchase"],
        "| Review creation:", item["review_creation"],
        "| Days before purchase:", item["difference"]
    )