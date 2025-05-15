from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.upload import router as upload_router  
from app.api.search import router as search_router
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI()

origins = ["http://localhost:3000"]
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

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}