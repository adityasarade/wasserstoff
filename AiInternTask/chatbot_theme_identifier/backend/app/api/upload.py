from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.file_handler import extract_chunks_from_file
from app.services.vector_store import save_vector_store

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    all_chunks = []

    # Extract chunks from each file
    for file in files:
        try:
            chunks = await extract_chunks_from_file(file)
            print(f"[DEBUG] Extracted chunks from {file.filename}: {len(chunks)}")
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"[ERROR] Failed to extract chunks from {file.filename}: {e}")

    if not all_chunks:
        return {"error": "No valid documents were processed."}

    # Store new chunks in vector DB
    save_vector_store(all_chunks)

    # Return only a success message; LLM runs later during search
    return {
        "message": f"✅ Stored {len(all_chunks)} chunks across {len({c['doc_id'] for c in all_chunks})} documents."
    }