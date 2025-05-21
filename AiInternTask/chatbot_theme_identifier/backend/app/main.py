from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.upload import router as upload_router  
from app.api.search import router as search_router
from app.api.docs import router as docs_router
from app.api.maintenance import router as maintenance_router
from app.services.vector_store import init_vector_store
from fastapi.middleware.cors import CORSMiddleware
import os
from app.config import params

app = FastAPI()

@app.on_event("startup")
def startup_initialize_vector_store():
    """
    On application startup, (re)create an empty vector store.
    This ensures no old documents persist across restarts.
    """
    init_vector_store()
            
@app.get("/")
def root():
    return JSONResponse({"status": "ok"})

origins = [
    "http://localhost:3000",
    "https://wasserstoff-qicf.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(maintenance_router, prefix="", tags=["maintenance"])
app.include_router(upload_router)  
app.include_router(search_router)
app.include_router(docs_router)  

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}