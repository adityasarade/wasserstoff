from fastapi import APIRouter, Query
from app.services.vector_store import search
from app.services.llm_service import query_llm
from typing import List, Optional
from app.config import params

router = APIRouter()

@router.get("/search/")
async def search_documents(
    query: str = Query(..., description="The search query"),
    top_k: int = Query(10, ge=1, description="Number of top results to return"),
    doc_ids: Optional[str] = Query(
        None,
        description="Comma-separated list of document IDs to restrict the search to"
    )
):
    # Turn “DOC001,DOC002” into ["DOC001","DOC002"]
    selected = doc_ids.split(",") if doc_ids else None
    
    # Perform the semantic search, with in-service multiplier logic & optional doc filtering
    raw_chunks = search(query, top_k=top_k, doc_ids=selected)

    if not raw_chunks:
        return {"error": "No relevant information found."}
    
    # Deduplicate by doc_id, keeping first occurrence
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

    # Prepare tabular response
    tabular = [
        {
            "Document ID": chunk["doc_id"],
            "Extracted Answer": chunk["text"],
            "Citation": f"Page {chunk['page']}, Sentence {chunk['sentence']}"
        }
        for chunk in top_chunks
    ]

    # Build context for theme synthesis
    context = "\n".join(
        f"{c['doc_id']} (Page {c['page']}, Sentence {c['sentence']}): {c['text']}"
        for c in top_chunks
    )

    # System prompt for synthesis
    system_prompt = params["prompts"]["search"]["system"]
    synthesized_summary = query_llm(system_prompt, context)

    return {
        "individual_results": tabular,
        "synthesized_summary": synthesized_summary
    }