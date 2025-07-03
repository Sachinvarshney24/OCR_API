#!/usr/bin/env python3
"""
OCR processing module: handles both image and PDF inputs,
applies preprocessing, runs Tesseract, and returns extracted text.
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import numpy as np
from io import BytesIO
import logging

from app.utils.preprocessing import preprocess_image, correct_rotation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def process_file(file):
    """
    Processes an uploaded file (PDF or image), performs OCR, and returns text.

    Args:
        file (UploadFile): Uploaded file from FastAPI endpoint.

    Returns:
        str: Combined extracted text from the file.
    """
    file_content = await file.read()
    extension = file.filename.split(".")[-1].lower()

    extracted_text = ""

    try:
        if extension == "pdf":
            pages = convert_from_bytes(file_content)
            logging.info(f"Processing PDF with {len(pages)} page(s).")
            for page_num, page in enumerate(pages, start=1):
                img_array = np.array(page)
                img_array = correct_rotation(img_array)
                processed_img = preprocess_image(img_array)
                page_text = pytesseract.image_to_string(processed_img)
                extracted_text += f"\n=== Page {page_num} ===\n{page_text}"
        else:
            image = Image.open(BytesIO(file_content))
            img_array = np.array(image)
            img_array = correct_rotation(img_array)
            processed_img = preprocess_image(img_array)
            extracted_text = pytesseract.image_to_string(processed_img)

    except Exception as e:
        logging.error(f"Failed during OCR processing: {e}")
        raise

    return extracted_text.strip()
