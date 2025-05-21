from fastapi import APIRouter
from app.services.vector_store import init_vector_store

router = APIRouter()

@router.post("/clear/")
async def clear_vector_store():
    """
    Clears and re-initializes the FAISS index and metadata.
    """
    init_vector_store()
    return {"message": "Vector store cleared."}