import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("THEO_OPENROUTER_MODEL_KEY")
MODEL_NAME = "openai/gpt-oss-120b:free"

def test_openrouter():
    print(f"Testing model: {MODEL_NAME}")
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are Theo, a Christian AI assistant."},
                {"role": "user", "content": "Hello! Give me a short Biblical word of encouragement."}
            ]
        }
    )
    
    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        print("\n--- Theo's Response ---")
        print(content)
        print("------------------------")
        print("\n✅ Connectivity test successful!")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_openrouter()
