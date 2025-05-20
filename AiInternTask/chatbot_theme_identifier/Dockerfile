# 1. Start from a Python base that we can apt-install into
FROM python:3.11-slim

# 2. Install Tesseract OCR and its dev libs
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      libtesseract-dev \
 && rm -rf /var/lib/apt/lists/*

# 3. Set working directory
WORKDIR /app

# 4. Copy only requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# 5. Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the application code, including params.yaml under app/
COPY app/params.yaml ./app/params.yaml
COPY app ./app

# 7. Expose the port and run uvicorn
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
