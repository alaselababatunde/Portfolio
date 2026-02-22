import os
import json
import httpx
from typing import AsyncGenerator, List, Dict
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self):
        self.api_key = os.getenv("DSTV_AI_SUPPORT_OPENROUTER_MODEL_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        # Using the specified free model
        self.model = "openai/gpt-oss-120b:free"
        self.site_url = "https://dstv-ai-support.example.com" # Required by OpenRouter
        self.site_name = "DStv AI Support" # Required by OpenRouter

    async def stream_chat(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream("POST", self.base_url, headers=headers, json=payload) as response:
                    if response.status_code != 200:
                        error_detail = await response.aread()
                        try:
                            error_json = json.loads(error_detail)
                            error_msg = error_json.get("error", {}).get("message", "Unknown error")
                            
                            if response.status_code == 429:
                                yield "I apologize, but my premium brain is currently taking a short breather (rate limit reached). Please try again in a few moments."
                            elif response.status_code == 401:
                                yield "Connection error: API key is invalid or expired."
                            else:
                                yield f"I'm having a little trouble connecting to my service (Error {response.status_code}: {error_msg}). Please try again soon."
                        except:
                            yield f"Error: {response.status_code} - Encountered an unexpected response format."
                        return

                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    content = data["choices"][0].get("delta", {}).get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                yield f"Connection Error: {str(e)}"

openrouter_client = OpenRouterClient()
