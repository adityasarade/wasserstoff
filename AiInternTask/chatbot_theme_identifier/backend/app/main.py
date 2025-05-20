from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.upload import router as upload_router  
from app.api.search import router as search_router
from app.api.docs import router as docs_router
from fastapi.middleware.cors import CORSMiddleware
import os
from app.config import params

app = FastAPI()

@app.on_event("startup")
def clear_vector_store_on_startup():
    vector_dir = params["paths"]["vector_store_dir"]
    index_path = os.path.join(vector_dir, params["paths"]["index_file"])
    meta_path  = os.path.join(vector_dir, params["paths"]["metadata_file"])
    for p in (index_path, meta_path):
        if os.path.exists(p):
            os.remove(p)
            
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
app.include_router(upload_router)  
app.include_router(search_router)
app.include_router(docs_router)  

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}