from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.file_handler import extract_text_from_file
from app.services.llm_service import query_llm, truncate_text

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            extracted_text = await extract_text_from_file(file)

            if extracted_text is None:
                results.append({
                    "filename": file.filename,
                    "error": "Unsupported file type"
                })
                continue

            system_prompt = "You are a helpful assistant that identifies the main theme or topic of a given document."
            truncated = truncate_text(extracted_text)
            llm_response = query_llm(system_prompt, truncated)

            results.append({
                "filename": file.filename,
                "llm_response": llm_response
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    return results