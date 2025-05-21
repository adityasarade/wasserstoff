import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config import params

router = APIRouter()

@router.post("/reset/")
def reset_vector_store():
    vector_dir = params["paths"]["vector_store_dir"]
    index_path = os.path.join(vector_dir, params["paths"]["index_file"])
    meta_path  = os.path.join(vector_dir, params["paths"]["metadata_file"])
    for p in (index_path, meta_path):
        if os.path.exists(p):
            os.remove(p)
    return JSONResponse({"message": "Knowledge base cleared."})
