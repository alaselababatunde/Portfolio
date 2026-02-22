import os
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List

from rag_engine import rag_engine
from openrouter_client import openrouter_client
from memory_manager import memory_manager
from search_tool import search_tool

app = FastAPI(title="DStv AI Support API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

SYSTEM_PROMPT = """You are DStv AI Support, a helpful and professional customer support representative for DStv.
Your tone is friendly, clear, practical, and human.

Rules:
1. Never say "as an AI".
2. Never mention internal systems.
3. Speak like real DStv support (e.g., "I can help you with that", "Let me check our guides for you").
4. Use the provided context to answer accurately.
5. Formatting: Use Markdown for all replies. Use bolding, lists, and headings for readability. Ensure tables are properly formatted if used.
6. Web Search: If the provided context does not contain enough information to answer the question, a web search will be provided. Use those results to assist the user.
7. If you still cannot find the answer, politely inform the user and suggest they contact DStv support via official channels like the DStv app or WhatsApp.

When answering, focus on providing direct, actionable advice to the user.
"""

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    user_message = request.message
    
    # 1. Search RAG
    rag_results = rag_engine.query(user_message)
    context = ""
    
    if rag_results:
        context = "\n".join([doc.page_content for doc in rag_results])
    
    # 2. If RAG results are weak or not found, try web search fallback
    # Increased threshold slightly to trigger search more proactively
    if not context or len(context) < 300:
        web_results = search_tool.search_web(user_message)
        if web_results:
            context += "\n\nWeb Search Results:\n"
            for res in web_results:
                context += f"- {res['title']}: {res['snippet']}\n"

    # 3. Retrieve Memory
    history = memory_manager.get_history(session_id)
    
    # 4. Prepare messages for AI
    current_context_prompt = f"Context Information:\n{context}\n\nUser Question: {user_message}"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Add relevant history (last 5 exchanges for context)
    for msg in history[-10:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": current_context_prompt})

    # Save user message to memory
    memory_manager.save_message(session_id, "user", user_message)

    async def response_generator():
        full_response = ""
        async for chunk in openrouter_client.stream_chat(messages):
            full_response += chunk
            yield chunk
        
        # Save assistant response to memory after stream finishes
        memory_manager.save_message(session_id, "assistant", full_response)

    return StreamingResponse(response_generator(), media_type="text/event-stream")

@app.get("/session")
async def create_session():
    return {"session_id": str(uuid.uuid4())}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Serve static files from frontend/dist
# This MUST be after all API routes to avoid shadowing
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")


