#!/usr/bin/env python3
"""
Train a text classification model on OCR-extracted bill text
from labeled PDF and image files.
"""

import os
import pandas as pd
import logging
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# ------------------------
# Configurable paths
# ------------------------
RAW_BILLS_DIR = os.path.join("data", "raw_bills")
LABELS_CSV_PATH = os.path.join("data", "labels.csv")
OUTPUT_MODEL_PATH = os.path.join("app", "models", "bill_model.pkl")

# ------------------------
# Setup logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def perform_ocr(file_path: str) -> str:
    """
    Runs OCR on a PDF or image file and returns extracted text.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""

    if ext == ".pdf":
        try:
            pages = convert_from_path(file_path)
            logging.info(f"OCR: Processing PDF {file_path} with {len(pages)} page(s).")
            for page_num, page in enumerate(pages, start=1):
                page_text = pytesseract.image_to_string(page)
                text += f"\n=== Page {page_num} ===\n{page_text}"
        except Exception as e:
            logging.warning(f"[PDF ERROR] Failed to process {file_path}: {e}")
    else:
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
        except Exception as e:
            logging.warning(f"[IMAGE ERROR] Failed to process {file_path}: {e}")

    return text

def main():
    # Check required files/folders
    if not os.path.exists(RAW_BILLS_DIR):
        logging.error(f"Raw bills directory not found: {RAW_BILLS_DIR}")
        return

    if not os.path.isfile(LABELS_CSV_PATH):
        logging.error(f"Labels CSV not found: {LABELS_CSV_PATH}")
        return

    # Load labeled data
    labels_df = pd.read_csv(LABELS_CSV_PATH)
    texts, categories = [], []

    logging.info("Starting OCR and dataset preparation...")

    for idx, row in labels_df.iterrows():
        bill_filename = row.get("filename")
        bill_category = row.get("category")
        bill_path = os.path.join(RAW_BILLS_DIR, bill_filename)

        if not os.path.isfile(bill_path):
            logging.warning(f"Missing bill file: {bill_path}, skipping.")
            continue

        ocr_text = perform_ocr(bill_path)
        if ocr_text.strip():
            texts.append(ocr_text)
            categories.append(bill_category)
        else:
            logging.warning(f"No text extracted from {bill_path}")

    if not texts:
        logging.error("No OCR text extracted; cannot train model.")
        return

    logging.info(f"OCR complete. Processed {len(texts)} documents.")

    # Vectorize text
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(texts)

    # Train model
    classifier = LogisticRegression(max_iter=500, random_state=42)
    classifier.fit(features, categories)

    # Save model and vectorizer
    os.makedirs(os.path.dirname(OUTPUT_MODEL_PATH), exist_ok=True)
    joblib.dump({"vectorizer": vectorizer, "model": classifier}, OUTPUT_MODEL_PATH)

    logging.info(f"✅ Model trained successfully and saved at: {OUTPUT_MODEL_PATH}")

if __name__ == "__main__":
    main()
