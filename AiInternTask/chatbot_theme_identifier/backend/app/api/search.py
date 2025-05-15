from fastapi import APIRouter, Query
from app.services.vector_store import search
from app.services.llm_service import query_llm
from typing import List
from app.core.config import params

router = APIRouter()

@router.get("/search/")
async def search_documents(query: str = Query(...), top_k: int = 10):
    # Fetch extra candidates based on multiplier from params
    multiplier = params["search"]["initial_top_k_multiplier"]
    raw_chunks = search(query, top_k=top_k * multiplier)
    
    # Deduplicate based on Document ID
    seen_doc_ids = set()
    unique_chunks = []
    for chunk in raw_chunks:
        if chunk["doc_id"] not in seen_doc_ids:
            seen_doc_ids.add(chunk["doc_id"])
            unique_chunks.append(chunk)

    # Filter out chunks with very short or uninformative text
    min_words = params["search"]["chunk_min_words"]
    filtered_chunks = [c for c in unique_chunks if len(c["text"].split()) >= min_words]

    # Pick top_k from filtered list
    top_chunks = filtered_chunks[:top_k]

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
    system_prompt = params["prompts"]["search"]["system"]
    synthesized_response = query_llm(system_prompt, context)

    return {
        "individual_results": tabular,
        "synthesized_summary": synthesized_response
    }