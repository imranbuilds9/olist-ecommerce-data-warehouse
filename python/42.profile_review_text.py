import csv
from collections import Counter

path = r"data\raw\olist_order_reviews_dataset.csv"

title_lengths = []
message_lengths = []

title_whitespace_only = 0
message_whitespace_only = 0

title_examples = Counter()
message_examples = Counter()

with open(path, encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        title = row["review_comment_title"]
        message = row["review_comment_message"]

        if title.strip():
            title_lengths.append(len(title))
            title_examples[title.strip()] += 1
        elif title:
            title_whitespace_only += 1

        if message.strip():
            message_lengths.append(len(message))
            message_examples[message.strip()] += 1
        elif message:
            message_whitespace_only += 1


def show_stats(name, values):
    print("\n", name)
    print("Non-empty records:", len(values))

    if values:
        print("Minimum length:", min(values))
        print("Maximum length:", max(values))
        print("Average length:", round(sum(values) / len(values), 2))


print("REVIEW TEXT PROFILE")

show_stats("TITLE", title_lengths)
show_stats("MESSAGE", message_lengths)

print("\nWhitespace-only titles:", title_whitespace_only)
print("Whitespace-only messages:", message_whitespace_only)

print("\nMost common titles:")
for text, count in title_examples.most_common(10):
    print(repr(text), ":", count)

print("\nMost common messages:")
for text, count in message_examples.most_common(10):
    print(repr(text), ":", count)