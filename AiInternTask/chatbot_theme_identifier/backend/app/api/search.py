from fastapi import APIRouter, Query
from typing import Optional
from app.services.vector_store import search
from app.services.llm_service import query_llm
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
    # 1) Parse optional doc filter
    selected = doc_ids.split(",") if doc_ids else None

    # 2) Vector search + initial rerank/filter
    raw_chunks = search(query, top_k=top_k, doc_ids=selected)
    if not raw_chunks:
        return {"error": "No relevant information found."}

    # 3) Dedupe & drop too-short chunks in one pass
    seen = set()
    min_words = params["search"]["chunk_min_words"]
    deduped = []
    for c in raw_chunks:
        if c["doc_id"] not in seen and len(c["text"].split()) >= min_words:
            seen.add(c["doc_id"])
            deduped.append(c)

    top_chunks = deduped[:top_k]

    # 4) Build the table rows
    extracted_table = [
        {
            "Document ID": c["doc_id"],
            "Extracted Answer": c["text"],
            "Citation": f"Page {c['page']}, Sentence {c['sentence']}"
        }
        for c in top_chunks
    ]

    # 5) Prepare LLM context for theme synthesis
    context = "\n".join(
        f"{c['doc_id']} (Pg {c['page']}, Sent {c['sentence']}): {c['text']}"
        for c in top_chunks
    )

    # 6) Call LLM once for cross-document themes
    system_prompt = params["prompts"]["search"]["system"]
    synthesized_summary = query_llm(system_prompt, context)

    # 7) Return exactly what the frontend needs
    return {
        "individual_results": extracted_table,
        "synthesized_summary": synthesized_summary
    }