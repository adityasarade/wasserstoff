from fastapi import APIRouter, Query
from app.services.vector_store import search
from app.services.llm_service import query_llm
from typing import List

router = APIRouter()

@router.get("/search/")
async def search_documents(query: str = Query(...), top_k: int = 10):
    top_chunks = search(query, top_k=top_k)

    if not top_chunks:
        return {"error": "No relevant information found."}

    # Prepare tabular response
    tabular = [
        {
            "Document ID": chunk["doc_id"],
            "Extracted Answer": chunk["text"],
            "Citation": f"Page {chunk['page']}, Sentence {chunk['sentence']}"
        }
        for chunk in top_chunks
    ]

    # Build context for LLM
    chunk_texts = [
        f"{c['doc_id']} (Page {c['page']}, Sentence {c['sentence']}): {c['text']}"
        for c in top_chunks
    ]
    context = "\n".join(chunk_texts)

    # System prompt for synthesis
    system_prompt = (
        "You are an AI assistant that synthesizes legal evidence into key themes.\n"
        "Given the following extracted facts from documents, group them into meaningful themes.\n"
        "Use the format:\n\n"
        "Theme 1 – [Title of theme]:\n"
        "Documents (DOC001, DOC003) explain ...\n\n"
    )

    # Call LLM with both prompts
    synthesized_response = query_llm(system_prompt, context)

    return {
        "individual_results": tabular,
        "synthesized_summary": synthesized_response
    }