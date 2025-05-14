from PIL import Image
import pytesseract
import pdfplumber
import io
from fastapi import UploadFile

async def extract_text_from_file(file: UploadFile) -> str | None:
    content = await file.read()
    filename = file.filename.lower()
    extracted_text = ""

    if filename.endswith(".pdf"):
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
        except Exception:
            pass  # fallback to OCR handled below if PDF text extraction fails

        if not extracted_text:  # fallback to OCR for scanned PDFs
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(content)
            for img in images:
                extracted_text += pytesseract.image_to_string(img)

    elif filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(io.BytesIO(content))
        extracted_text = pytesseract.image_to_string(image)

    else:
        return None

    return extracted_text.strip() if extracted_text else None