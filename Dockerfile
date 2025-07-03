FROM python:3.10

RUN apt-get update && apt-get install -y tesseract-ocr poppler-utils

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
