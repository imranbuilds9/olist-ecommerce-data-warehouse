import csv
from collections import Counter

path = r"data\raw\olist_geolocation_dataset.csv"

total_rows = 0
missing = Counter()
blank = Counter()

zip_prefixes = set()
states = Counter()

latitude_values = []
longitude_values = []

invalid_latitude = 0
invalid_longitude = 0

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    print("Columns:", reader.fieldnames)

    for row in reader:
        total_rows += 1

        zip_code = row["geolocation_zip_code_prefix"].strip()
        lat = row["geolocation_lat"].strip()
        lng = row["geolocation_lng"].strip()
        city = row["geolocation_city"].strip()
        state = row["geolocation_state"].strip()

        if not zip_code:
            missing["zip_prefix"] += 1
        else:
            zip_prefixes.add(zip_code)

        if not lat:
            missing["latitude"] += 1
        else:
            try:
                latitude_values.append(float(lat))
            except ValueError:
                invalid_latitude += 1

        if not lng:
            missing["longitude"] += 1
        else:
            try:
                longitude_values.append(float(lng))
            except ValueError:
                invalid_longitude += 1

        if not city:
            missing["city"] += 1

        if not state:
            missing["state"] += 1
        else:
            states[state] += 1

print("\n" + "=" * 55)
print("GEOLOCATION PROFILE")
print("=" * 55)

print("Total rows:", total_rows)
print("Distinct ZIP prefixes:", len(zip_prefixes))

print("\nMissing values:", dict(missing))
print("Invalid latitude values:", invalid_latitude)
print("Invalid longitude values:", invalid_longitude)

if latitude_values:
    print("\nLatitude minimum:", min(latitude_values))
    print("Latitude maximum:", max(latitude_values))

if longitude_values:
    print("Longitude minimum:", min(longitude_values))
    print("Longitude maximum:", max(longitude_values))

print("\nState distribution:")
for state, count in states.most_common():
    print(state, ":", count)