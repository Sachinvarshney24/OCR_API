#!/usr/bin/env python3
"""
Generates synthetic PDF bills with many categories and realistic data,
saving them to data/raw_bills for OCR & ML training/testing.
"""

import os
import random
from faker import Faker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

fake = Faker()

categories = {
    "books": ["novel", "dictionary", "atlas", "comic", "journal"],
    "grocery": ["rice", "milk", "bread", "sugar", "lentils", "spices"],
    "electronics": ["phone", "charger", "laptop", "headphones", "tablet"],
    "medicines": ["paracetamol", "azithromycin", "aspirin", "ibuprofen", "cough syrup"],
    "fashion": ["t-shirt", "jeans", "jacket", "dress", "skirt", "shirt"],
    "stationery": ["notebook", "pen", "marker", "folder", "eraser", "ruler"],
    "kitchenware": ["saucepan", "knife", "cutting board", "blender", "frying pan"],
    "toys": ["lego set", "teddy bear", "board game", "puzzle", "remote car"],
    "sports": ["football", "basketball", "yoga mat", "dumbbells", "skipping rope"],
    "hardware": ["hammer", "screwdriver", "wrench", "drill", "pliers"],
    "furniture": ["chair", "table", "sofa", "bookshelf", "bed frame"],
    "office equipment": ["printer", "scanner", "keyboard", "monitor", "mouse"],
    "cosmetics": ["lipstick", "foundation", "eyeliner", "moisturizer", "perfume"],
    "gardening": ["shovel", "watering can", "plant pot", "fertilizer", "garden gloves"],
    "automotive": ["engine oil", "car battery", "brake pads", "air filter", "spark plug"],
    "pets": ["dog food", "cat litter", "bird cage", "fish tank", "pet shampoo"]
}

output_dir = "data/raw_bills"
os.makedirs(output_dir, exist_ok=True)

def generate_bill(idx):
    category = random.choice(list(categories.keys()))
    supplier = fake.company()
    customer = fake.name()
    date = fake.date()
    gst_number = f"{random.randint(10,99)}{fake.lexify(text='?????')}{random.randint(1000,9999)}A1Z5"
    receipt_no = f"INV-{random.randint(10000,99999)}"

    items = []
    for _ in range(random.randint(3, 6)):
        item_name = random.choice(categories[category])
        qty = random.randint(1, 5)
        price = round(random.uniform(10, 3000), 2)
        items.append((item_name, qty, price))

    filename = f"{idx:04d}_{category}.pdf"
    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"INVOICE / BILL - {category.upper()}")
    y -= 70  # Increased spacing for better OCR

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Date: {date}")
    y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Supplier: {supplier}")
    y -= 20
    c.drawString(50, y, f"Customer: {customer}")
    y -= 20
    c.drawString(50, y, f"GST Number: {gst_number}")
    y -= 20
    c.drawString(50, y, f"Receipt Number: {receipt_no}")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.setFont("Helvetica", 12)

    total = 0
    for item_name, qty, price in items:
        y -= 20
        c.drawString(50, y, item_name)
        c.drawString(250, y, str(qty))
        c.drawString(300, y, f"{price:.2f}")
        total += qty * price

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"TOTAL: {total:.2f}")
    c.save()

    return {
        "filename": filename,
        "category": category,
        "date": date,
        "supplier": supplier,
        "customer": customer,
        "gst_number": gst_number,
        "receipt_number": receipt_no,
        "total": f"{total:.2f}"
    }

if __name__ == "__main__":
    import csv
    num_bills = 50
    csv_labels_path = os.path.join(output_dir, "labels.csv")
    with open(csv_labels_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "category", "date", "supplier", "customer",
            "gst_number", "receipt_number", "total"
        ])
        writer.writeheader()
        for i in range(num_bills):
            label = generate_bill(i)
            writer.writerow(label)

    print(f"✅ Generated {num_bills} synthetic bills and labels CSV at {csv_labels_path}")
