# Python base
FROM python:3.11-slim

# Install Tesseract OCR, Poppler (for pdf2image), and FAISS dependency
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      tesseract-ocr \
      libtesseract-dev \
      poppler-utils \
      libomp-dev \
 && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK punkt + punkt_tab into writable location
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data'); nltk.download('punkt_tab', download_dir='/usr/local/share/nltk_data')"

# Point NLTK to the pre-downloaded data
ENV NLTK_DATA=/usr/local/share/nltk_data

# Create writable data directory and fix permissions
RUN mkdir -p /app/data && chmod 777 /app/data

ENV ENV=production

# Copy in your backend code tree
COPY app ./app

# Expose & run
ENV PORT=7860
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]