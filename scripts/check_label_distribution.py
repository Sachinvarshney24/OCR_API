import csv
from collections import Counter

labels_csv = "data/labels.csv"

with open(labels_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    categories = [row['category'] for row in reader]

counts = Counter(categories)

print("\n📊 Category distribution in labels.csv:")
for category, count in sorted(counts.items()):
    print(f"{category:20} -> {count} samples")

if not counts:
    print("\n🚨 labels.csv is empty or missing expected data.")
