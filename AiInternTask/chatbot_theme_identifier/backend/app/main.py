from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import pdfplumber
import io
import shutil
import os
from app.services.llm_service import query_llm

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename.lower()
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file
    try:
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        return JSONResponse({"error": f"File saving failed: {str(e)}"}, status_code=500)

    extracted_text = ""

    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(io.BytesIO(content))
            extracted_text = pytesseract.image_to_string(image)

        else:
            return JSONResponse({"error": "Unsupported file type"}, status_code=400)

        return {
            "filename": file.filename,
            "status": "saved",
            "preview": extracted_text[:500]  # Send first 500 chars for now
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
@app.post("/test-llm/")
async def test_llm():
    system_prompt = "You are a helpful assistant who summarizes user queries."
    user_prompt = "Explain the concept of few-shot learning in simple terms."
    
    try:
        response = query_llm(system_prompt, user_prompt)
        return {"response": response}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)