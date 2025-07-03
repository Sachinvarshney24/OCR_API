# OCR & ML-Based Bill Parsing API

This project provides an automated backend API using OCR and machine learning to extract structured data from bill images or PDFs.

# 🧾 OCR & ML-Based Bill Parsing API

This project provides a powerful backend REST API that uses Optical Character Recognition (OCR) and Machine Learning (ML) to automatically extract structured data from scanned bills (PDFs or images) and classify them into categories like fashion, grocery, medicines, electronics, and more.

---

##  Key Features

✅ Upload scanned or synthetic bills (PDF/JPG/PNG)  
✅ Extract fields like date, total amount, and detailed line items  
✅ Predict purchase category using a trained ML model  
✅ Outputs structured JSON data  
✅ Ready for containerized deployment with Docker

---

## 🏗️ Project Structure

OCR_API_Project/
├── app/ # FastAPI app, routes, ML models, parsers
├── data/ # Raw, synthetic, and test bills
├── scripts/ # Dataset generation, testing, utilities
│ └── experimental/ # Optional scripts for OCR and manual labeling
├── requirements.txt # Python dependencies
├── Dockerfile # For containerized deployment
└── README.md # You're here!



---

## ⚙️ Quick Setup

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd OCR_API_Project


2️⃣ Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


3️⃣ Train the ML model

Generate a synthetic dataset:
-- python scripts/generate_synthetic_bills.py

Train the category classifier:
-- python scripts/train_model.py

4️⃣ Start the API

uvicorn app.main:app --reload

Access interactive API docs at: http://localhost:8000/docs

 API Usage
POST /upload
Upload a bill (PDF/image) → returns extracted data and predicted category.

Example request with curl:

bash
Copy
Edit
curl -X POST "http://localhost:8000/upload" -F "file=@data/test_bills/fashion_test.pdf"
📦 Example API Response
json
Copy
Edit
{
  "status": "success",
  "data": {
    "date": "2023-06-15",
    "total": "5894.00",
    "items": [
      {"description": "t-shirt", "quantity": "2", "price": "499.00"},
      {"description": "jeans", "quantity": "1", "price": "1999.00"}
    ],
    "predicted_category": "fashion"
  }
}
📜 Scripts
scripts/generate_synthetic_bills.py
→ Creates synthetic bills with realistic category-specific items + a labeled CSV for training.

scripts/train_model.py
→ Trains a text classifier using OCR-extracted data from labeled bills.

scripts/create_test_bills.py
→ Quickly generates small sample bills for testing your API.

scripts/experimental/generate_labels.py
→ [Optional] Generates a CSV of filenames for manually labeling real scanned bills.

scripts/experimental/test_ocr.py
→ [Optional] Debugs OCR output on a sample bill image or PDF.

🐳 Docker Deployment
To run your API in a container:

bash
Copy
Edit
docker build -t bill-parser-api .
docker run -p 8000:8000 bill-parser-api
Then access your API docs at: http://localhost:8000/docs

✅ How It Works
1️⃣ OCR Engine

Uses Tesseract OCR (via pytesseract) + OpenCV preprocessing.

Converts PDFs to images when needed.

2️⃣ Parsing

Extracts date, total amount, line items with quantity, description, and price.

3️⃣ ML Model

A Logistic Regression classifier with TF-IDF text features predicts purchase categories.

4️⃣ API

Built with FastAPI → fast, async, easy to scale.

📂 Dataset
Synthetic bills generated with realistic items, totals, and labels → saved in data/synthetic_bills/.

Training labels CSV saved as labels.csv in the same folder.

Ready to train your model out of the box.

👨‍💻 Development & Debugging Tips
✅ Use scripts/experimental/test_ocr.py to inspect OCR output on individual samples.

✅ Check data/test_bills/ to quickly test your end-to-end pipeline without retraining.

✅ Add more categories or customize item lists in scripts/generate_synthetic_bills.py to fit your needs.

🙌 Acknowledgements
Tesseract OCR

spaCy (optional for advanced NLP)

FastAPI

ReportLab for synthetic bill generation



