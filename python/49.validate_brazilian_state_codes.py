import csv
from collections import Counter

valid_states = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF",
    "ES", "GO", "MA", "MT", "MS", "MG", "PA",
    "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
    "RO", "RR", "SC", "SP", "SE", "TO"
}

datasets = [
    (
        "CUSTOMERS",
        r"data\raw\olist_customers_dataset.csv",
        "customer_state"
    ),
    (
        "SELLERS",
        r"data\raw\olist_sellers_dataset.csv",
        "seller_state"
    ),
    (
        "GEOLOCATION",
        r"data\raw\olist_geolocation_dataset.csv",
        "geolocation_state"
    ),
    (
        "ORDERS",
        r"data\raw\olist_orders_dataset.csv",
        None
    )
]

for name, path, state_column in datasets:

    if state_column is None:
        print("\n", name, "- No state column; skipped.")
        continue

    counts = Counter()
    missing = 0

    with open(path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            state = row[state_column].strip()

            if not state:
                missing += 1
            else:
                counts[state] += 1

    invalid = {
        state: count
        for state, count in counts.items()
        if state not in valid_states
    }

    print("\n" + "=" * 50)
    print(name)
    print("TOTAL RECORDS:", sum(counts.values()) + missing)
    print("DISTINCT STATE CODES:", len(counts))
    print("MISSING STATE VALUES:", missing)
    print("INVALID STATE CODES:", invalid)

    print("STATE DISTRIBUTION:")

    for state, count in sorted(counts.items()):
        print(state, ":", count)