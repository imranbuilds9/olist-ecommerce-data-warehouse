import csv
from collections import Counter, defaultdict

path = r"data\raw\olist_geolocation_dataset.csv"

total_rows = 0
exact_rows = Counter()
zip_counts = Counter()
zip_coordinates = defaultdict(set)
zip_cities = defaultdict(set)
zip_states = defaultdict(set)

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1

        zip_code = row["geolocation_zip_code_prefix"]
        lat = float(row["geolocation_lat"])
        lng = float(row["geolocation_lng"])
        city = row["geolocation_city"]
        state = row["geolocation_state"]

        exact_key = (
            zip_code,
            lat,
            lng,
            city,
            state
        )

        exact_rows[exact_key] += 1

        zip_counts[zip_code] += 1
        zip_coordinates[zip_code].add((lat, lng))
        zip_cities[zip_code].add(city)
        zip_states[zip_code].add(state)


duplicate_exact_rows = sum(
    count - 1
    for count in exact_rows.values()
    if count > 1
)

multiple_coordinate_zips = sum(
    1 for coordinates in zip_coordinates.values()
    if len(coordinates) > 1
)

multiple_city_zips = sum(
    1 for cities in zip_cities.values()
    if len(cities) > 1
)

multiple_state_zips = sum(
    1 for states in zip_states.values()
    if len(states) > 1
)


print("\nTOTAL ROWS:", total_rows)
print("DISTINCT ZIP PREFIXES:", len(zip_counts))
print("EXACT DUPLICATE ROWS:", duplicate_exact_rows)

print(
    "\nZIP PREFIXES WITH MULTIPLE COORDINATES:",
    multiple_coordinate_zips
)

print(
    "ZIP PREFIXES WITH MULTIPLE CITY NAMES:",
    multiple_city_zips
)

print(
    "ZIP PREFIXES WITH MULTIPLE STATE CODES:",
    multiple_state_zips
)


print("\n--- TOP 15 ZIP PREFIXES BY ROW COUNT ---")

for zip_code, count in zip_counts.most_common(15):
    print(
        "ZIP:", zip_code,
        "| Rows:", count,
        "| Unique coordinates:", len(zip_coordinates[zip_code]),
        "| Cities:", len(zip_cities[zip_code]),
        "| States:", len(zip_states[zip_code])
    )


print("\n--- FIRST 10 ZIP PREFIXES WITH MULTIPLE STATES ---")

shown = 0

for zip_code, states in zip_states.items():
    if len(states) > 1:
        print(
            "\nZIP:", zip_code,
            "| States:", sorted(states),
            "| Cities:", sorted(zip_cities[zip_code])
        )

        shown += 1

        if shown == 10:
            break