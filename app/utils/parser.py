#!/usr/bin/env python3
"""
Parses OCR-extracted text to identify structured fields
such as date, total amount, and detailed item lines.
"""

import re
import logging

from app.utils.ml_model import predict_category

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Lines containing these keywords will be excluded as metadata
IRRELEVANT_KEYWORDS = [
    "gst", "total", "receipt number", "invoice", "inv-", "tax", "grand total"
]

# Regex pattern for item lines like "t-shirt 2 499.00"
ITEM_REGEX = r"^([A-Za-z0-9\s\-]+?)\s+(\d+)\s+(\d+(?:\.\d{1,2})?)$"

# Updated regex: matches optional 'Date:' prefix + ISO/DD/MM/YYYY formats
DATE_REGEX = r"\b(?:date[:\-]?\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b"

def parse_text(text: str) -> dict:
    """
    Extracts structured information from OCR text, including date, total,
    and detailed items with qty, description, and price.

    Args:
        text (str): The OCR-extracted raw text.

    Returns:
        dict: Parsed data with date, total, and item details.
    """
    logging.info("OCR TEXT:\n" + text)

    # ✅ Validate input type and emptiness
    if not isinstance(text, str) or not text.strip():
        logging.warning("Invalid or empty text received for parsing.")
        return {}

    # ✅ Search entire OCR text for date (not line by line)
    date_match = re.search(DATE_REGEX, text, re.IGNORECASE)

    # Extract total in formats like TOTAL: 1234.56
    total_pattern = r"\btotal\s*[:\-]?\s*(\d+(?:\.\d{1,2})?)\b"
    total_match = re.search(total_pattern, text, re.IGNORECASE)

    # Process text line by line for items
    lines = text.splitlines()
    item_details = []

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        # Skip irrelevant metadata
        if any(keyword in clean_line.lower() for keyword in IRRELEVANT_KEYWORDS):
            continue

        # Match item pattern
        match = re.match(ITEM_REGEX, clean_line)
        if match:
            desc = match.group(1).strip()
            qty = match.group(2)
            price = match.group(3)
            item_details.append({
                "description": desc,
                "quantity": qty,
                "price": price
            })

    parsed_data = {
        "date": date_match.group(1) if date_match else None,
        "total": total_match.group(1) if total_match else None,
        "items": item_details
    }

    logging.debug(f"Parsed data: {parsed_data}")
    return parsed_data
