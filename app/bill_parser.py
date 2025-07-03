#!/usr/bin/env python3
"""
Example script demonstrating how to use predictor module
to classify a list of items into a purchase category.
"""

from app.utils.predictor import predict_category

def main():
    # Example item text (from OCR)
    sample_items_text = "milk, bread, butter"

    predicted_category = predict_category(sample_items_text)
    print(f"Predicted category: {predicted_category}")

if __name__ == "__main__":
    main()
