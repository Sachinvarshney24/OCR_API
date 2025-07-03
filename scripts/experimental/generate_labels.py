#!/usr/bin/env python3
"""
Generates a labeled CSV file with placeholders for manual annotation
of bill data such as category, date, supplier, and items.
"""

import os
import csv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

BILLS_DIR = os.path.join("data", "raw_bills")
OUTPUT_CSV = os.path.join("data", "labeled_data.csv")

def generate_label_csv():
    """
    Lists all bill files and generates a CSV file with placeholder columns
    for manual labeling.
    """
    if not os.path.isdir(BILLS_DIR):
        logging.error(f"Raw bills directory does not exist: {BILLS_DIR}")
        return

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    bill_files = [
        f for f in os.listdir(BILLS_DIR)
        if f.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png'))
    ]

    with open(OUTPUT_CSV, mode="w", newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "filename",
            "category",
            "date",
            "supplier",
            "customer",
            "total",
            "gst_number",
            "receipt_number",
            "items"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for bill in bill_files:
            writer.writerow({
                "filename": bill,
                "category": "",           # Fill manually (e.g., "groceries")
                "date": "",
                "supplier": "",
                "customer": "",
                "total": "",
                "gst_number": "",
                "receipt_number": "",
                "items": ""               # e.g., "item1, item2"
            })

    logging.info(f"Labeled CSV generated with {len(bill_files)} entries at {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_label_csv()
