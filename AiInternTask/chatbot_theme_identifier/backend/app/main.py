from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.llm_service import query_llm, truncate_text
from app.services.vector_store import search
from app.services.file_handler import extract_text_from_file
from pydantic import BaseModel
from typing import List
import os

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            extracted_text = await extract_text_from_file(file)

            if not extracted_text:
                results.append({
                    "filename": file.filename,
                    "error": "Unsupported or unreadable file"
                })
                continue

            system_prompt = "You are a helpful assistant that identifies the main theme or topic of a given document."
            truncated_text = truncate_text(extracted_text)
            llm_response = query_llm(system_prompt, truncated_text)

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

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search/")
async def semantic_search(req: SearchRequest):
    try:
        results = search(req.query, top_k=req.top_k)
        return {"query": req.query, "results": results}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)