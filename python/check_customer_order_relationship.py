
import csv
from collections import Counter

customers_path = r"data\raw\olist_customers_dataset.csv"
orders_path = r"data\raw\olist_orders_dataset.csv"

customer_ids = set()

with open(customers_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        customer_id = row["customer_id"].strip()
        if customer_id:
            customer_ids.add(customer_id)

order_count_by_customer = Counter()
missing_customer_ids = 0
orders_without_customer_record = 0
total_orders = 0

with open(orders_path, encoding="utf-8-sig", newline="") as file:
    for row in csv.DictReader(file):
        total_orders += 1
        customer_id = row["customer_id"].strip()

        if not customer_id:
            missing_customer_ids += 1
        elif customer_id not in customer_ids:
            orders_without_customer_record += 1
        else:
            order_count_by_customer[customer_id] += 1

customers_with_orders = len(order_count_by_customer)
customers_with_multiple_orders = sum(
    1 for count in order_count_by_customer.values() if count > 1
)
maximum_orders = max(order_count_by_customer.values(), default=0)

print("Total orders checked:", total_orders)
print("Customer records available:", len(customer_ids))
print("Orders with missing customer_id:", missing_customer_ids)
print("Orders referencing nonexistent customer records:", orders_without_customer_record)
print("Customer records linked to at least one order:", customers_with_orders)
print("Customer records linked to multiple orders:", customers_with_multiple_orders)
print("Maximum orders linked to one customer record:", maximum_orders)
