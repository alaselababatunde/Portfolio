import os
import io
import tempfile
import logging
import traceback
from fastapi import FastAPI, Header, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import pipeline
from langdetect import detect, DetectorFactory
from PIL import Image
from smebuilder_vector import retriever  # Local vector retriever

# ==============================
# Logging Setup
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DevAssist")

# ==============================
# FastAPI Init
# ==============================
app = FastAPI(title="DevAssist AI Backend")

@app.get("/")
async def root():
    return {"status": "DevAssist AI Backend running"}

# ==============================
# Auth Configuration
# ==============================
PROJECT_API_KEY = os.getenv("PROJECT_API_KEY", "devassist-secret")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
SPITCH_API_KEY = os.getenv("SPITCH_API_KEY")

def check_auth(authorization: str | None):
    """Bearer token validator."""
    if not PROJECT_API_KEY:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    if token != PROJECT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid token")

# ==============================
# Global Error Handler
# ==============================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}")
    return JSONResponse(status_code=500, content={"error": str(exc)})

# ==============================
# Request Schemas
# ==============================
class ChatRequest(BaseModel):
    question: str

class AutoDocRequest(BaseModel):
    code: str

class SMERequest(BaseModel):
    user_prompt: str

# ==============================
# HuggingFace Pipelines
# ==============================
if not HF_TOKEN:
    logger.warning("⚠️ No Hugging Face token found. Private/gated models may fail.")
else:
    logger.info("✅ Hugging Face token detected and ready.")

HF_MODELS = {
    "chat": "meta-llama/Llama-3.1-8B-Instruct",
    "autodoc": "Salesforce/codegen-2B-mono",
    "sme": "deepseek-ai/deepseek-coder-1.3b-instruct"
}

def safe_pipeline(task: str, model: str, fallback="gpt2"):
    try:
        return pipeline(task, model=model, token=HF_TOKEN)
    except Exception as e:
        logger.warning(f"Failed to load {model}: {e} → Falling back to {fallback}")
        return pipeline(task, model=fallback)

chat_pipe = safe_pipeline("text-generation", HF_MODELS["chat"])
autodoc_pipe = safe_pipeline("text-generation", HF_MODELS["autodoc"])
sme_pipe = safe_pipeline("text-generation", HF_MODELS["sme"])

# ==============================
# Helper: Text Generation
# ==============================
def run_pipeline(pipe, prompt: str, max_tokens=512):
    """Run a text-generation pipeline with proper error capture."""
    try:
        output = pipe(prompt, max_new_tokens=max_tokens)
        if isinstance(output, list) and len(output) > 0:
            result = output[0].get("generated_text", "").strip()
        else:
            result = str(output).strip()

        logger.info(f"\n--- PROMPT ---\n{prompt}\n--- OUTPUT ---\n{result}\n--- END ---")

        if not result:
            return {"success": False, "error": "⚠️ LLM returned empty output."}
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        return {
            "success": False,
            "error": f"⚠️ LLM error: {str(e)}",
            "trace": traceback.format_exc(),
        }

# ==============================
# Audio Processing Helper
# ==============================
async def process_audio(file: UploadFile, lang_hint: str | None = None):
    import spitch
    spitch_client = spitch.Spitch()
    suffix = os.path.splitext(file.filename)[1] or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
        tf.write(await file.read())
        tmp_path = tf.name

    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()

    try:
        resp = spitch_client.speech.transcribe(
            content=audio_bytes, language=lang_hint or "en"
        )
    except Exception as e:
        logger.warning(f"Speech API failed: {e}")
        resp = {"text": ""}

    transcription = getattr(resp, "text", "") or (resp.get("text", "") if isinstance(resp, dict) else "")
    detected_lang = "en"
    try:
        detected_lang = detect(transcription) if transcription.strip() else "en"
    except Exception:
        pass

    # Optional translation
    translation = transcription
    if detected_lang != "en":
        try:
            translation_resp = spitch_client.text.translate(
                text=transcription, source=detected_lang, target="en"
            )
            translation = getattr(translation_resp, "text", "") or translation_resp.get("text", "")
        except Exception:
            translation = transcription

    return transcription, detected_lang, translation

# ==============================
# Endpoints
# ==============================
@app.post("/chat")
async def chat_endpoint(req: ChatRequest, authorization: str | None = Header(None)):
    check_auth(authorization)
    prompt = f"You are a helpful developer assistant. Question:\n{req.question}\nAnswer clearly:"
    result = run_pipeline(chat_pipe, prompt)
    return result

@app.post("/autodoc")
async def autodoc_endpoint(req: AutoDocRequest, authorization: str | None = Header(None)):
    check_auth(authorization)
    prompt = f"Generate Markdown documentation for the following Python code:\n{req.code}\nDocumentation:"
    result = run_pipeline(autodoc_pipe, prompt)
    return result

@app.post("/sme/generate")
async def sme_generate_endpoint(req: SMERequest, authorization: str | None = Header(None)):
    check_auth(authorization)
    try:
        context_docs = retriever.get_relevant_documents(req.user_prompt)
        context = "\n".join([doc.page_content for doc in context_docs]) if context_docs else "No extra context"
        prompt = f"Generate production-grade frontend code based on this:\n{req.user_prompt}\nContext:\n{context}\nOutput:"
        result = run_pipeline(sme_pipe, prompt)
        return result
    except Exception as e:
        return {"success": False, "error": f"⚠️ LLM error: {str(e)}", "trace": traceback.format_exc()}

@app.post("/sme/speech-generate")
async def sme_speech_endpoint(file: UploadFile = File(...), lang_hint: str | None = None, authorization: str | None = Header(None)):
    check_auth(authorization)
    transcription, detected_lang, translation = await process_audio(file, lang_hint)
    try:
        context_docs = retriever.get_relevant_documents(translation)
        context = "\n".join([doc.page_content for doc in context_docs]) if context_docs else "No extra context"
        prompt = f"Generate production-ready frontend code for this idea:\n{translation}\nContext:\n{context}\nOutput:"
        result = run_pipeline(sme_pipe, prompt)
        return {
            "success": True,
            "transcription": transcription,
            "detected_language": detected_lang,
            "translation": translation,
            "output": result.get("data", ""),
        }
    except Exception as e:
        return {"success": False, "error": f"⚠️ LLM error: {str(e)}", "trace": traceback.format_exc()}

# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
