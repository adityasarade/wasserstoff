from PIL import Image
import pytesseract
import pdfplumber
import io
from fastapi import UploadFile
from pdf2image import convert_from_bytes
import uuid
import nltk
from nltk.tokenize import sent_tokenize
from app.config import params
import shutil     

# Download tokenizer if missing
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

TESSERACT_AVAILABLE = shutil.which("tesseract") is not None
if not TESSERACT_AVAILABLE:
    print("⚠️ Warning: Tesseract not found in PATH — OCR will be skipped.")

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess PIL Image for better OCR accuracy: convert to grayscale and apply threshold.
    """
    gray = image.convert("L")  # grayscale
    thresh = params["ocr"]["threshold"]
    bw = gray.point(lambda x: 0 if x < 140 else 255, '1')  # simple binary threshold
    return bw

async def extract_chunks_from_file(file: UploadFile) -> list[dict]:
    """
    Extract sentence-level chunks with metadata from PDF or image file.
    Returns a list of dicts: {'doc_id', 'filename', 'page', 'sentence', 'text'}.
    """
    content = await file.read()
    filename = file.filename.lower()
    file_id = f"DOC{str(uuid.uuid4())[:5].upper()}"  # Short custom doc ID
    chunks = []

    def chunk_sentences(text, doc_id, page_number, filename):
        sentences = sent_tokenize(text)
        for sent_number, sentence in enumerate(sentences, start=1):
            clean_sentence = sentence.strip().replace("\n", " ")
            if clean_sentence:
                chunks.append({
                    "doc_id": doc_id,
                    "filename": filename,
                    "page": page_number,
                    "sentence": sent_number,
                    "text": clean_sentence,
                    "text_length": len(clean_sentence)
                })
                
    dpi = params["ocr"]["dpi"]
    psm = params["ocr"]["tesseract_psm"]
    
    if filename.endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                print(f"🧾 PDF opened: {filename}")
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()
                    if page_text:
                        print(f"📄 Page {page_number} text preview: {repr(page_text[:100])}")
                        chunk_sentences(page_text, file_id, page_number, file.filename)
                    else:
                        print(f"⚠️ Page {page_number} has no text.")
                        if TESSERACT_AVAILABLE:                       
                            print("   ↪️ Falling back to OCR on this page")
                            img = page.to_image(resolution=dpi).original
                            img = preprocess_image(img)
                            try:
                                ocr_text = pytesseract.image_to_string(img, config=f'--psm {psm}')
                                print(f"🖼️ OCR text from page {page_number}: {repr(ocr_text[:100])}")
                                chunk_sentences(ocr_text, file_id, page_number, file.filename)
                            except pytesseract.TesseractNotFoundError:
                                print(f"❌ Tesseract not found at OCR time.")
                        else:
                            print("   ↪️ Skipping OCR (tesseract missing)")
        except Exception as e:
            print(f"❌ PDFPlumber error for {filename}: {e}")
            if TESSERACT_AVAILABLE:                           
                print("📸 OCR fallback for entire PDF...")
                images = convert_from_bytes(content, dpi=dpi)
                for page_number, img in enumerate(images, start=1):
                    img = preprocess_image(img)
                    try:
                        ocr_text = pytesseract.image_to_string(img, config=f'--psm {psm}')
                        print(f"🖼️ OCR text from page {page_number}: {repr(ocr_text[:100])}")
                        chunk_sentences(ocr_text, file_id, page_number, file.filename)
                    except pytesseract.TesseractNotFoundError:
                        print(f"❌ Tesseract not found at OCR time.")
            else:
                print("   ↪️ Skipping full-PDF OCR (tesseract missing)")

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        print(f"🖼️ Image file detected: {filename}")
        if TESSERACT_AVAILABLE:                              
            image = Image.open(io.BytesIO(content))
            image = preprocess_image(image)
            try:
                ocr_text = pytesseract.image_to_string(image, config=f'--psm {psm}')
                print(f"🖨️ OCR text preview: {repr(ocr_text[:100])}")
                chunk_sentences(ocr_text, file_id, page_number=1, filename=file.filename)
            except pytesseract.TesseractNotFoundError:
                print(f"❌ Tesseract not found at OCR time.")
        else:
            print("   ↪️ Skipping OCR on image (tesseract missing)")

    print(f"✅ Extracted {len(chunks)} chunks from {filename}")
    return chunks