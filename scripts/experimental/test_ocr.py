#!/usr/bin/env python3
"""
Quick script for testing OCR preprocessing and Tesseract output
on a single sample bill image.
"""

import os
import cv2
import pytesseract
import logging

from app.utils.preprocessing import preprocess_image, correct_rotation

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Replace with your own sample image path
SAMPLE_IMAGE_PATH = os.path.join("data", "raw_bills", "bill1.jpeg")

def test_ocr_pipeline(image_path: str):
    """
    Loads an image, preprocesses it, runs OCR, and prints the result.

    Args:
        image_path (str): Path to the bill image file.
    """
    if not os.path.isfile(image_path):
        logging.error(f"Image file not found: {image_path}")
        return

    img = cv2.imread(image_path)
    if img is None:
        logging.error(f"Failed to load image: {image_path}")
        return

    logging.info("Starting rotation correction...")
    img = correct_rotation(img)

    logging.info("Starting image preprocessing...")
    processed_img = preprocess_image(img)

    debug_output = "processed_debug.jpg"
    cv2.imwrite(debug_output, processed_img)
    logging.info(f"Preprocessed image saved for inspection: {debug_output}")

    logging.info("Performing OCR...")
    extracted_text = pytesseract.image_to_string(processed_img)

    print("\n===== OCR TEXT =====")
    print(extracted_text)
    print("====================")

if __name__ == "__main__":
    test_ocr_pipeline(SAMPLE_IMAGE_PATH)
