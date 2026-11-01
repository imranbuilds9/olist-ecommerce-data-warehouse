import csv
from decimal import Decimal

path = r"data\raw\olist_order_payments_dataset.csv"

target_orders = {
    "c5bdd8ef3c0ec420232e668302179113",
    "3ee6513ae7ea23bdfab5b9ab60bffcb5",
    "6e864b3f0ec71031117ad4cf46b7f2a1",
    "fb265b2dc558a56445dfc48f8224e201",
    "d642656598ae928a250620315d19e87e",
    "8272b63d03f5f79c56e9e4120aec44ef"
}

payments_by_order = {}

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = row["order_id"]

        if order_id in target_orders:
            payments_by_order.setdefault(order_id, []).append(row)

for order_id in sorted(target_orders):

    payments = payments_by_order.get(order_id, [])

    print("\n" + "=" * 60)
    print("ORDER:", order_id)

    if not payments:
        print("No payment records found.")
        continue

    payment_total = sum(
        (Decimal(row["payment_value"]) for row in payments),
        Decimal("0")
    )

    print("Number of payment records:", len(payments))

    for payment in payments:
        print(
            "Sequential:", payment["payment_sequential"],
            "| Type:", payment["payment_type"],
            "| Installments:", payment["payment_installments"],
            "| Value: R$", payment["payment_value"]
        )

    print("Total payment value: R$", payment_total)