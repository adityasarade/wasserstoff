# 1. Python base
FROM python:3.11-slim

# 2. Install Tesseract OCR
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      libtesseract-dev \
 && rm -rf /var/lib/apt/lists/*

# 3. Set workdir
WORKDIR /app

# 4. Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy in your backend code tree
COPY AiInternTask/chatbot_theme_identifier/backend/app ./app

# 6. Expose & run
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]