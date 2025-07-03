#!/usr/bin/env python3
"""
Generates a small set of manually crafted test bills for quick API evaluation.
Each bill simulates a real purchase invoice in different categories.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Output folder for test bills
output_dir = "data/test_bills"
os.makedirs(output_dir, exist_ok=True)

# Sample bills: (bill content, filename)
sample_bills = [
    (
        """INVOICE / BILL - FASHION
Date: 2023-06-15
Supplier: Elite Fashions Ltd.
Customer: Priya Verma
GST Number: 45abcde2345A1Z5
Receipt Number: INV-12345

Item              Qty    Price
t-shirt           2      499.00
jeans             1      1999.00
kurta             3      799.00

TOTAL: 5894.00""",
        "fashion_test.pdf"
    ),
    (
        """INVOICE / BILL - MEDICINES
Date: 2024-03-20
Supplier: MediCare Distributors
Customer: Ravi Sharma
GST Number: 67fghij6789A1Z5
Receipt Number: INV-45678

Item              Qty    Price
paracetamol       2      25.00
azithromycin      1      55.00
aspirin           1      35.00

TOTAL: 140.00""",
        "medicines_test.pdf"
    ),
    (
        """INVOICE / BILL - ELECTRONICS
Date: 2022-11-10
Supplier: Tech Hub Pvt Ltd
Customer: Anjali Rao
GST Number: 32klmno1234A1Z5
Receipt Number: INV-78901

Item              Qty    Price
phone             1      25000.00
charger           1      799.00
power bank        1      1599.00

TOTAL: 27398.00""",
        "electronics_test.pdf"
    ),
    (
        """INVOICE / BILL - TOYS
Date: 2021-08-05
Supplier: Kids World
Customer: Kabir Malhotra
GST Number: 19pqrstu5678A1Z5
Receipt Number: INV-90123

Item              Qty    Price
lego set          1      2999.00
teddy bear        2      899.00
board game        1      1499.00

TOTAL: 6296.00""",
        "toys_test.pdf"
    ),
    (
        """INVOICE / BILL - KITCHENWARE
Date: 2024-01-25
Supplier: HomeEssentials Ltd.
Customer: Ritu Shah
GST Number: 81vwxyz9876A1Z5
Receipt Number: INV-34567

Item              Qty    Price
saucepan          1      799.00
knife             2      299.00
cutting board     1      499.00

TOTAL: 1896.00""",
        "kitchenware_test.pdf"
    ),
]

# Generate PDFs for each sample bill
for text, filename in sample_bills:
    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica", 12)

    for line in text.splitlines():
        c.drawString(50, y, line.strip())
        y -= 20  # Line spacing

    c.save()
    print(f"✅ Saved test bill: {filepath}")

print("\n🎉 All test bills generated successfully!")
