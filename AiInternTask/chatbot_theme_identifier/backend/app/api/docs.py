from fastapi import APIRouter
from app.services.vector_store import load_vector_store

router = APIRouter()

@router.get("/documents/")
async def list_documents():
    """
    Return a list of {doc_id, filename} for all loaded documents.
    """
    _, chunks = load_vector_store()
    if not chunks:
        return {"documents": []}
    # Dedupe by doc_id, keep first filename seen
    docs = {}
    for c in chunks:
        docs.setdefault(c["doc_id"], c["filename"])

    return {"documents": [
        {"doc_id": doc_id, "filename": fname}
        for doc_id, fname in docs.items()
    ]}