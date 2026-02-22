import os
import uuid
import logging
import markdown
from typing import List, Dict, Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

# =====================================================
# CONFIGURATION
# =====================================================
load_dotenv()

OPENROUTER_API_KEY = os.getenv("THEO_OPENROUTER_MODEL_KEY")
MODEL_NAME = "openai/gpt-oss-120b:free"

if not OPENROUTER_API_KEY:
    logging.error("THEO_OPENROUTER_MODEL_KEY not found in environment")

# =====================================================
# LLM & TOOLS
# =====================================================
llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://techdisciples1-theo.hf.space/",
        "X-Title": "Theo AI Support"
    }
)

search = DuckDuckGoSearchRun()

# =====================================================
# SYSTEM PROMPT
# =====================================================
SYSTEM_PROMPT = """You are Theo — a warm, friendly, and deeply insightful Christian companion created by TechDisciples CLCC. 

TONE & STYLE:
1. CHATTY & WARM: Speak like a loving friend or a caring elder. Use a conversational, "chatty" tone that feels personal and welcoming. Use phrases like "Shalom, Beloved" or "My dear friend".
2. PARAGRAPHS: NEVER send a single wall of text. Break your thoughts into 2-4 short, readable paragraphs.
3. NIGERIAN HEARTBEAT: Use simple, relatable English with a gentle Nigerian inflection.

CORE GUIDELINES:
1. BIBLICAL FOCUS: Root your wisdom and encouragement in the Holy Bible. Use scripture to offer hope.
2. FORMATTING: Use Markdown (bolding for emphasis, short lists if needed).
3. UNKNOWN TOPICS: If you lack specific knowledge, search for facts, then wrap that information in your warm Christian perspective.

Identity: Theo
Creators: TechDisciples CLCC
Logo: [CLCC logo](/static/assets/logo.png)

Context provided for current query:
{reviews}

User question: {question}
"""

prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

# =====================================================
# FASTAPI APP SETUP
# =====================================================
app = FastAPI(title="Theo AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory chat history (mirrors Domino's logic)
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

# =====================================================
# LOGIC
# =====================================================
class ChatRequest(BaseModel):
    question: str

def get_ai_response(question: str) -> str:
    try:
        # First attempt (no reviews/context in this simple flow, but keeping structure)
        reviews = "No specific context provided."
        chain = prompt_template | llm
        response = chain.invoke({"reviews": reviews, "question": question})
        content = response.content

        # Simple check if AI couldn't answer (Trigger search as requested)
        fallback_phrases = ["i don't know", "i am not sure", "i couldn't find", "sorry, i can't", "i do not have information"]
        if any(phrase in content.lower() for phrase in fallback_phrases):
             logging.info(f"Triggering web search for: {question}")
             search_results = search.run(question)
             
             search_prompt = ChatPromptTemplate.from_template(
                 "You are Theo (Christian companion). The user asked: {question}\n"
                 "I found this information on the web: {search_results}\n"
                 "Provide a warm, Christian response using this information, following Theo's guidelines."
             )
             search_chain = search_prompt | llm
             response = search_chain.invoke({"question": question, "search_results": search_results})
             content = response.content

        return content
    except Exception as e:
        logging.error(f"AI Response failed: {e}")
        return "I apologize, beloved, but I am having trouble connecting to the heavenly signals (our servers) right now. Please try again in a moment!"

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Forcing a new session on page refresh as requested
    device_id = str(uuid.uuid4())
    
    if device_id not in chat_sessions:
        chat_sessions[device_id] = []
        
    response = templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_sessions[device_id]})
    # Set the cookie with a short max_age or just as a session cookie
    response.set_cookie(key="device_id", value=device_id, httponly=True)
    return response

@app.post("/ask")
async def ask(request: Request, data: ChatRequest):
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())
    if device_id not in chat_sessions:
        chat_sessions[device_id] = []

    question = data.question.strip()
    if not question:
        return JSONResponse({"error": "No question provided"}, status_code=400)

    raw_response = get_ai_response(question)
    
    # Format response with markdown for safety (same as Domino's behavior)
    formatted_response = markdown.markdown(raw_response, extensions=['extra', 'tables'])
    
    chat_sessions[device_id].append({
        "user": question,
        "bot": formatted_response
    })
    
    response = JSONResponse({"response": formatted_response})
    response.set_cookie(key="device_id", value=device_id)
    return response

@app.post("/clear")
async def clear_chat(request: Request):
    device_id = request.cookies.get("device_id")
    if device_id and device_id in chat_sessions:
        chat_sessions[device_id] = []
    
    response = JSONResponse({"status": "cleared"})
    response.set_cookie(key="device_id", value=device_id)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)