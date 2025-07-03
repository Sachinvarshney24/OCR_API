#!/usr/bin/env python3
"""
FastAPI application entry point for the Bill Parsing API.
"""

from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Bill Parsing API",
    description="A backend API for extracting structured data from scanned bills using OCR and ML.",
    version="1.0.0"
)

app.include_router(router)
