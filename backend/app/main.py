# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from app.huggingface_api import HuggingFaceAPI

app = FastAPI()

# Configurar CORS específicamente para el frontend
origins = [
    "http://localhost:3000",  # URL del frontend en desarrollo
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    prompt: str
    model_type: str = "general"

@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}

@app.post("/api/prompt")
async def process_prompt(request: PromptRequest):
    try:
        hf = HuggingFaceAPI()
        response = hf.regular_prompt(request.prompt, request.model_type)
        print(f"Processing prompt: {request.prompt} with model: {request.model_type}")
        print(f"Response: {response}")
        return response
    except Exception as e:
        print(f"Error processing prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)