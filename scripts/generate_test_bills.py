#!/usr/bin/env python3
"""
Generates 10 test bills with diverse categories, improved Date placement,
and visible formatting so OCR reliably captures all key fields.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

output_dir = "data/test_bills"
os.makedirs(output_dir, exist_ok=True)

sample_bills = [
    (
        """INVOICE / BILL - KITCHENWARE

Supplier: HomeEssentials Ltd.
Customer: Ritu Shah
Date: 2024-01-25
GST Number: 81vwxyz9876A1Z5
Receipt Number: INV-34567

Item              Qty    Price
saucepan          1      799.00
knife             2      299.00
cutting board     1      499.00

TOTAL: 1896.00""",
        "kitchenware_test.pdf"
    ),
    (
        """INVOICE / BILL - ELECTRONICS

Supplier: Tech Hub Pvt Ltd.
Customer: Anjali Rao
Date: 2022-11-10
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
        """INVOICE / BILL - MEDICINES

Supplier: MediCare Distributors
Customer: Ravi Sharma
Date: 2024-03-20
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
        """INVOICE / BILL - FASHION

Supplier: Elite Fashions Ltd.
Customer: Priya Verma
Date: 2023-06-15
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
        """INVOICE / BILL - GROCERY

Supplier: FreshMart
Customer: Sunita Mehta
Date: 2023-09-05
GST Number: 21qwert6789A1Z5
Receipt Number: INV-55555

Item              Qty    Price
rice              5      50.00
milk              3      30.00
sugar             2      40.00

TOTAL: 370.00""",
        "grocery_test.pdf"
    ),
    (
        """INVOICE / BILL - SPORTS

Supplier: SportsPro India
Customer: Arjun Kapoor
Date: 2022-12-18
GST Number: 12asdfg5678A1Z5
Receipt Number: INV-88888

Item              Qty    Price
football          1      999.00
basketball        1      1199.00
yoga mat          2      499.00

TOTAL: 3196.00""",
        "sports_test.pdf"
    ),
    (
        """INVOICE / BILL - TOYS

Supplier: FunZone Toys
Customer: Neha Kumar
Date: 2023-04-22
GST Number: 54zxcvb0987A1Z5
Receipt Number: INV-33333

Item              Qty    Price
lego set          1      2999.00
teddy bear        2      899.00
board game        1      1499.00

TOTAL: 6296.00""",
        "toys_test.pdf"
    ),
    (
        """INVOICE / BILL - STATIONERY

Supplier: OfficeSupplies Co.
Customer: Rakesh Singh
Date: 2023-02-10
GST Number: 09lkjhgf2345A1Z5
Receipt Number: INV-22222

Item              Qty    Price
notebook          5      50.00
pen               10     20.00
marker            3      40.00

TOTAL: 490.00""",
        "stationery_test.pdf"
    ),
    (
        """INVOICE / BILL - HARDWARE

Supplier: BuildPro Hardware
Customer: Manish Patel
Date: 2024-05-02
GST Number: 77mnopq3456A1Z5
Receipt Number: INV-99999

Item              Qty    Price
hammer            1      350.00
wrench            2      299.00
drill             1      2999.00

TOTAL: 3947.00""",
        "hardware_test.pdf"
    ),
    (
        """INVOICE / BILL - FURNITURE

Supplier: ComfortHome Furnishings
Customer: Meena Joshi
Date: 2023-07-14
GST Number: 88rstuvw4567A1Z5
Receipt Number: INV-77777

Item              Qty    Price
chair             2      1499.00
table             1      3999.00
bookshelf         1      2499.00

TOTAL: 9496.00""",
        "furniture_test.pdf"
    )
]

for text, filename in sample_bills:
    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 120  # Generous top margin for Date line

    lines = text.splitlines()
    for line in lines:
        line_strip = line.strip()
        # Highlight Date line for better OCR detection
        if line_strip.lower().startswith("date:"):
            c.setFont("Helvetica-Bold", 14)
        else:
            c.setFont("Helvetica", 12)
        c.drawString(50, y, line_strip)
        y -= 22  # Line spacing

    c.save()
    print(f"✅ Saved test bill: {filepath}")

print("\n🎉 All 10 test bills generated successfully!")
