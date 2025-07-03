#!/usr/bin/env python3
"""
Image preprocessing utilities: noise reduction, thresholding, and skew correction
to improve OCR accuracy on scanned bills.
"""

import cv2
import numpy as np
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def preprocess_image(img: np.ndarray) -> np.ndarray:
    """
    Converts image to grayscale, reduces noise, and applies adaptive thresholding.

    Args:
        img (np.ndarray): Input color image (BGR).

    Returns:
        np.ndarray: Preprocessed binary image suitable for OCR.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce noise while preserving edges
    filtered = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # Improve text contrast with adaptive thresholding
    binary = cv2.adaptiveThreshold(
        filtered, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31, C=2
    )

    return binary

def correct_rotation(img: np.ndarray) -> np.ndarray:
    """
    Detects skew angle from text contours and corrects image rotation.

    Args:
        img (np.ndarray): Input image (BGR or grayscale).

    Returns:
        np.ndarray: Deskewed image.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    coords = np.column_stack(np.where(binary_inv > 0))
    if coords.shape[0] == 0:
        logging.warning("No text found for rotation correction; returning original image.")
        return img

    rect = cv2.minAreaRect(coords)
    angle = rect[-1]

    # Adjust the angle for correct rotation
    angle = -(90 + angle) if angle < -45 else -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    logging.debug(f"Corrected image rotation by {angle:.2f} degrees.")
    return rotated
