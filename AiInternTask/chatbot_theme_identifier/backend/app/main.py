from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.upload import router as upload_router  
from app.api.search import router as search_router  

app = FastAPI()

# Include routes
app.include_router(upload_router)  
app.include_router(search_router)  

@app.get("/")
def read_root():
    return {"message": "Server is up and running!"}