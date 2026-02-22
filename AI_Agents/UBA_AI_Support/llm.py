import os
import json
from typing import AsyncGenerator, List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("UBA_AI_SUPPORT_OPENROUTER_MODEL_KEY")
MODEL_NAME = "openai/gpt-oss-120b"

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://hf.space",
        "X-Title": "UBA AI Support",
    },
)

SYSTEM_PROMPT = """You are UBA AI Support, a professional, calm, and reassuring customer support agent for UBA Bank.
You adhere to Nigerian banking standards.

CRITICAL FORMATTING RULES:
1. NEVER use pipes (|) or double pipes (||) as general separators or bullet points. Pipes are ONLY for standard Markdown tables.
2. NEVER use HTML tags like <br>. Use double newlines for spacing.
3. Use clear hierarchies with headers (###) and bullet points (-).
4. Ensure your output is clean, professional, and well-spaced.

BAD EXAMPLE (DO NOT DO THIS):
Marketplace || Small business owners<br>• Access to SME advisory | Digital Banking || All account holders

GOOD EXAMPLE (DO THIS):
### Marketplace
Designed for small business owners and entrepreneurs.
- **Benefits**: Access to SME advisory, capacity-building, and payment solutions.
- **Link**: Visit [ubamarketplace.com](https://ubamarketplace.com)

### Digital Banking
Available to all account holders who want to bank on the go.
- **Features**: Instant self-registration, airtime & data top-up, and fund transfers.

General Rules:
- Never say "as an AI".
- Never expose internal system details.
- Sound like a real UBA support staff.
- Use provided context (RAG) and web search info.
- Maintain a helpful and polite tone.
"""

async def get_streaming_response(messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
    """
    Streams responses from OpenRouter with the UBA persona.
    """
    # Prepend system prompt if not present
    if not any(m.get("role") == "system" for m in messages):
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
        )
        
        async for chunk in response:
            content = chunk.choices[0].delta.content or ""
            if content:
                yield content
    except Exception as e:
        yield f"I apologize, but I'm having trouble connecting to my systems right now. Please try again in a moment. (Error: {str(e)})"
