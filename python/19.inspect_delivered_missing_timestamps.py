
import csv

path = r"data\raw\olist_orders_dataset.csv"

count = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        if (
            row["order_status"].strip() == "delivered"
            and not row["order_delivered_customer_date"].strip()
        ):
            count += 1

            print("Order ID:", row["order_id"])
            print("Purchase:", row["order_purchase_timestamp"])
            print("Approved:", row["order_approved_at"])
            print("Carrier:", row["order_delivered_carrier_date"])
            print("Delivered:", row["order_delivered_customer_date"])
            print("Estimated delivery:", row["order_estimated_delivery_date"])
            print("-" * 40)

print("Total delivered orders missing delivery timestamp:", count)
