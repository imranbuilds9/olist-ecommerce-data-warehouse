
import csv
from collections import defaultdict

path = r"data\raw\olist_customers_dataset.csv"

customer_ids = set()
unique_to_customer_ids = defaultdict(set)
missing_customer_id = 0
missing_unique_id = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        customer_id = row["customer_id"].strip()
        unique_id = row["customer_unique_id"].strip()

        if not customer_id:
            missing_customer_id += 1
        else:
            customer_ids.add(customer_id)

        if not unique_id:
            missing_unique_id += 1
        elif customer_id:
            unique_to_customer_ids[unique_id].add(customer_id)

reused_identities = {
    unique_id: ids
    for unique_id, ids in unique_to_customer_ids.items()
    if len(ids) > 1
}

print("Unique customer_id values:", len(customer_ids))
print("Distinct customer_unique_id values:", len(unique_to_customer_ids))
print("Missing customer_id values:", missing_customer_id)
print("Missing customer_unique_id values:", missing_unique_id)
print("Underlying identities with multiple customer records:", len(reused_identities))

if reused_identities:
    print("\nFirst five examples:")
    for unique_id, ids in list(reused_identities.items())[:5]:
        print(
            "customer_unique_id:",
            unique_id,
            "| customer_id count:",
            len(ids)
        )
