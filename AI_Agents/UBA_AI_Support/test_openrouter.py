import asyncio
import os
from dotenv import load_dotenv
from llm import get_streaming_response

# Load environment variables
load_dotenv()

async def test_openrouter():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        return

    print(f"Testing OpenRouter connection with key: {api_key[:8]}...")
    
    messages = [
        {"role": "user", "content": "Hello, are you online?"}
    ]

    print("\nSending request...")
    try:
        async for chunk in get_streaming_response(messages):
            print(chunk, end="", flush=True)
        print("\n\nTest completed successfully.")
    except Exception as e:
        print(f"\nError during test: {e}")

if __name__ == "__main__":
    asyncio.run(test_openrouter())
