#!/usr/bin/env python3
"""
Defines API routes for uploading bills and returning structured parsed data.
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.utils.ocr_engine import process_file
from app.utils.parser import parse_text
from app.utils.ml_model import predict_category
import logging
import traceback

router = APIRouter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@router.post("/upload", response_class=JSONResponse)
async def upload_bill(file: UploadFile = File(...)):
    """
    Uploads a bill (image or PDF), processes it with OCR,
    extracts structured fields, predicts purchase category,
    and returns the results in JSON format.
    """
    try:
        logging.info(f"Received file: {file.filename}")

        # Step 1: Extract raw text from the uploaded file
        raw_text = await process_file(file)

        # Step 2: Parse structured fields from raw OCR text
        parsed_data = parse_text(raw_text)

        # Step 3: Predict category based on extracted items
        items = parsed_data.get("items", [])
        

        if isinstance(items, list) and items and isinstance(items[0], dict):
            # Convert dicts to meaningful strings for prediction input
            combined_items_text = " ".join(
                f"{item['description']} {item['quantity']} {item['price']}" for item in items
            )
        else:
            combined_items_text = " ".join(items) if isinstance(items, list) else str(items)

        predicted_category = predict_category(combined_items_text)
        parsed_data["predicted_category"] = predicted_category

        # Log raw OCR text for debugging purposes
        logging.debug("\n========== OCR RAW TEXT ==========\n%s\n==================================", raw_text)

        return {"status": "success", "data": parsed_data}

    except Exception as e:
        logging.error("Error while processing uploaded bill: %s", e)
        traceback.print_exc()
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
