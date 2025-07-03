#!/usr/bin/env python3
"""
Load the trained vectorizer and classifier model
for predicting bill categories from OCR text.
"""

import os
import joblib
import logging

MODEL_PATH = os.path.join("app", "models", "bill_model.pkl")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if not os.path.isfile(MODEL_PATH):
    raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}. Please train it first.")

with open(MODEL_PATH, "rb") as f:
    model_data = joblib.load(f)

vectorizer = model_data.get("vectorizer")
classifier = model_data.get("model")

if vectorizer is None or classifier is None:
    raise ValueError("Vectorizer or classifier missing in saved model file.")

def predict_category(text: str) -> str:
    """
    Predicts the category of a bill based on OCR-extracted text.
    
    Args:
        text (str): The OCR output text.
    
    Returns:
        str: Predicted bill category label.
    """
    if not text.strip():
        logging.warning("Empty text received for prediction.")
        return "unknown"

    transformed_text = vectorizer.transform([text])
    prediction = classifier.predict(transformed_text)[0]
    return prediction
