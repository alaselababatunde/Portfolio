import os
import json
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from llm import get_streaming_response
from rag import rag_system
from web_search import perform_web_search
from memory import memory_system

app = FastAPI(title="UBA AI Support")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    user_query = request.message
    
    try:
        # 1. Get history
        history = memory_system.get_history(session_id)
        
        # 2. Query RAG
        context = ""
        try:
            context = rag_system.query(user_query)
        except Exception as e:
            print(f"RAG Error: {e}")
            context = "" # Fallback to empty context
            
        # 3. If RAG context is weak, try web search
        web_context = ""
        if len(context) < 100:
            try:
                web_context = await perform_web_search(user_query)
            except Exception as e:
                print(f"Web Search Error: {e}")
                web_context = ""

        # 4. Prepare prompt
        augmented_query = user_query
        if context or web_context:
            augmented_query = f"Context from UBA Documentation:\n{context}\n\nWeb Search Info:\n{web_context}\n\nUser Question: {user_query}"
        
        # 5. Add to memory
        memory_system.add_message(session_id, "user", user_query)
        
        # 6. Stream response
        async def event_generator():
            # First send the session_id
            yield f"data: {json.dumps({'session_id': session_id})}\n\n"
            
            full_response = ""
            messages_for_llm = history[:-1] + [{"role": "user", "content": augmented_query}]
            
            async for chunk in get_streaming_response(messages_for_llm):
                full_response += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            
            # Save assistant response to memory
            memory_system.add_message(session_id, "assistant", full_response)
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        print(f"Endpoint Error: {e}")
        async def error_generator():
            yield f"data: {json.dumps({'content': 'I am sorry, but I encountered an internal error. Please try again later.'})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(error_generator(), media_type="text/event-stream")


# The frontend should be built and placed in a 'dist' folder or served directly if in dev
if os.path.exists("./frontend/dist"):
    app.mount("/", StaticFiles(directory="./frontend/dist", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
