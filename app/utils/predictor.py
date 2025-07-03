#!/usr/bin/env python3
"""
Predicts the purchase category based on OCR-extracted item text.
"""

import os
import pickle
import logging

MODEL_PATH = os.path.join("app", "models", "bill_model.pkl")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}. Please train the model first.")

with open(MODEL_PATH, "rb") as f:
    model_data = pickle.load(f)

vectorizer, classifier = model_data.get("vectorizer"), model_data.get("model")

if vectorizer is None or classifier is None:
    raise ValueError("Vectorizer or classifier is missing in the saved model file.")

def predict_category(item_text: str) -> str:
    """
    Predicts the bill category from item descriptions.

    Args:
        item_text (str): Combined item text extracted from a bill.

    Returns:
        str: Predicted category label.
    """
    if not item_text.strip():
        logging.warning("Empty item text received for category prediction.")
        return "unknown"

    transformed = vectorizer.transform([item_text])
    prediction = classifier.predict(transformed)[0]

    logging.debug(f"Predicted category: {prediction}")
    return prediction
