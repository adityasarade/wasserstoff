from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.file_handler import extract_chunks_from_file
from app.services.vector_store import save_vector_store
from app.services.summarizer import group_chunks_by_doc_id, summarize_documents

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

    # Step 1: Store new chunks in vector DB
    save_vector_store(all_chunks)

    # Step 2: Group the flat list of chunks by document ID
    grouped = group_chunks_by_doc_id(all_chunks)

    # Step 3: Summarize each document and synthesize themes
    individual_summaries, synthesized_summary = summarize_documents(grouped)

    return {
        "document_table": individual_summaries,
        "synthesized_summary": synthesized_summary
    }