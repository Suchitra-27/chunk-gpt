
from fastapi import FastAPI
from interfaces.api_routes import router as api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Chunk GPT is running"}
