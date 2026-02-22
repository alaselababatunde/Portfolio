import os
import logging
import json
from openai import OpenAI
from rag import RagEngine
from memory import MemoryManager
from duckduckgo_search import DDGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("TESCO_AI_SUPPORT_OPENROUTER_MODEL_KEY")
        if not self.api_key:
            logger.warning("TESCO_AI_SUPPORT_OPENROUTER_MODEL_KEY not set. LLM calls will fail.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://hf.co/spaces/alaselababatunde/Tesco_AI_Support",
                "X-Title": "Tesco AI Support"
            }
        )
        # Primary model as requested
        self.primary_model = "openai/gpt-oss-120b:free"
        # Fallback model if primary gives 404/policy error
        self.fallback_model = "google/gemini-2.0-flash-lite-preview-02-05:free"
        
        self.rag = RagEngine()
        self.memory = MemoryManager()

    def _web_search(self, query):
        """Perform a web search if RAG context is insufficient."""
        try:
            logger.info(f"Performing web search for: {query}")
            with DDGS() as ddgs:
                search_query = f"Tesco {query}"
                results = list(ddgs.text(search_query, max_results=3))
                if results:
                    return "\n\n".join([f"Web Info: {r['body']}" for r in results])
        except Exception as e:
            logger.error(f"Web search failed: {e}")
        return ""

    def generate_response(self, session_id, user_message):
        # 1. Retrieve Context
        try:
            results = self.rag.retrieve(user_message, n_results=5)
            retrieved_texts = results['documents'][0] if results.get('documents') else []
            context_str = "\n\n".join([t for t in retrieved_texts if t])
            
            if not context_str or len(context_str) < 150:
                web_info = self._web_search(user_message)
                if web_info:
                    context_str = f"{context_str}\n\n[RECENT WEB UPDATES]\n{web_info}".strip()
        except Exception as e:
            logger.error(f"RAG Retrieval error: {e}")
            context_str = ""

        # 2. History
        try:
            history = self.memory.get_history(session_id, limit=10)
        except Exception as e:
            logger.error(f"Memory error: {e}")
            history = []

        # 3. System Prompt
        system_prompt = f"""You are Tesco Support, a helpful and professional customer service agent.

CORE STYLE:
- British English, polite, natural.
- Use the CONTEXT DATA to answer. If it contains [RECENT WEB UPDATES], prioritize that for up-to-date facts.
- If unsure, suggest checking www.tesco.com or their helpline.
- DO NOT mention you are an AI or using search.

FORMATTING:
- Use clear PARAGRAPHS separated by blank lines.
- Use **bold** for key names, prices, or buttons.
- Use bullet points (-) for lists.

CONTEXT DATA:
{context_str}
"""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        full_response = ""
        
        # 4. Stream Response (Strictly using requested model)
        model_to_use = self.primary_model
        
        try:
            stream = self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
                    
        except Exception as e:
            error_msg = str(e)
            logger.error(f"LLM attempt with {model_to_use} failed: {error_msg}")
            
            # Catch the specific OpenRouter 'Data Policy' or 404 error
            if "data policy" in error_msg.lower() or "404" in error_msg:
                yield "\n\n**Error:** It seems your OpenRouter account is blocking free models due to privacy settings.\n\nPlease go to **[OpenRouter Privacy Settings](https://openrouter.ai/settings/privacy)** and enable:\n- **'Free endpoints that may train on inputs'**\n- **'Free endpoints that may publish prompts'**"
            else:
                yield f"I'm sorry, I'm having trouble connecting to the service. (Issue: {error_msg[:100]}...)"
        
        # 5. Save Interaction
        if full_response:
            try:
                self.memory.add_message(session_id, "user", user_message)
                self.memory.add_message(session_id, "assistant", full_response)
            except Exception as e:
                logger.error(f"Memory update failed: {e}")
