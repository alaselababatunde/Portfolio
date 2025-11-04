# =====================================================
# Tech Disciples AI Backend
# =====================================================

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import logging
import os

from huggingface_hub import login
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from transformers import pipeline

# =====================================================
# CONFIGURATION
# =====================================================
API_SECRET = "techdisciplesai404"
PRIMARY_MODEL = "meta-llama/Llama-3.1-8B"
FALLBACK_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
DEVICE = 0 if torch.cuda.is_available() else -1

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TechDisciplesAI")

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(title="Tech Disciples AI", version="3.1")

# ✅ Enable CORS (allow all origins for now; can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Change this to your frontend URL when known
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# MODEL LOADING FUNCTION
# =====================================================
def load_model(model_name, token=None):
    try:
        logger.info(f"🚀 Attempting to load model: {model_name}")
        text_gen = pipeline(
            "text-generation",
            model=model_name,
            device=DEVICE,
            max_new_tokens=1024,
            temperature=0.4,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            token=token,  # ✅ modern auth argument
        )
        logger.info(f"✅ Loaded model successfully: {model_name}")
        return HuggingFacePipeline(pipeline=text_gen)
    except Exception as e:
        logger.error(f"❌ Failed to load {model_name}: {e}")
        return None

# =====================================================
# LOAD TOKEN + MODEL
# =====================================================
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if hf_token:
    try:
        login(token=hf_token)
        logger.info("🔐 Hugging Face token authenticated.")
    except Exception as e:
        logger.warning(f"⚠️ Failed to log in: {e}")
else:
    logger.warning("⚠️ No HUGGINGFACEHUB_API_TOKEN found.")

llm = load_model(PRIMARY_MODEL, token=hf_token)

if llm is None:
    logger.warning("⚠️ Falling back to Mistral 7B due to model load issue...")
    llm = load_model(FALLBACK_MODEL, token=hf_token)

# =====================================================
# MEMORY + PROMPT
# =====================================================
memory = ConversationBufferMemory(memory_key="conversation_history")

prompt_template = """
You are Tech Disciples AI — a warm, spiritual, and knowledgeable conversational AI built
to give Biblical guidance and Christian-based reflections. You speak with empathy, wisdom,
and a natural tone — never robotic. Always connect your points to scripture or Christian principles
when relevant.

Conversation so far:
{conversation_history}

User: {query}
Tech Disciples AI (respond with warmth, depth, and Biblical understanding):
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["conversation_history", "query"]
)

chain = LLMChain(prompt=prompt, llm=llm, memory=memory) if llm else None

# =====================================================
# REQUEST MODEL
# =====================================================
class QueryInput(BaseModel):
    query: str
    session_id: str | None = "default"

# =====================================================
# ROUTES
# =====================================================
@app.get("/")
async def root():
    return {"message": "✅ Tech Disciples AI is online and ready."}

@app.post("/ai-chat")
async def ai_chat(data: QueryInput, x_api_key: str = Header(None)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")

    if not chain:
        raise HTTPException(status_code=500, detail="Model not initialized")

    try:
        response = chain.run(query=data.query.strip())
        return {"reply": response.strip()}
    except Exception as e:
        logger.error(f"⚠️ Model runtime error: {e}")
        raise HTTPException(status_code=500, detail=f"Model failed to respond — {e}")
