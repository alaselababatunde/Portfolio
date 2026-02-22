from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from llm import LLMClient
import logging
from dotenv import load_dotenv

load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tesco AI Support API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM Client
try:
    llm_client = LLMClient()
except Exception as e:
    logger.error(f"Failed to initialize LLM Client: {e}")
    llm_client = None

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Tesco AI Support Backend"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not llm_client:
        raise HTTPException(status_code=500, detail="LLM Backend not initialized")
    
    return StreamingResponse(
        llm_client.generate_response(request.session_id, request.message),
        media_type="text/event-stream"
    )

# Serve Frontend Static Files
# Mount assets Folder
if os.path.exists("frontend/dist/assets"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Serve index.html for SPA routing or clean entry
    if os.path.exists("frontend/dist/index.html"):
        return FileResponse("frontend/dist/index.html")
    return {"error": "Frontend not built"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
