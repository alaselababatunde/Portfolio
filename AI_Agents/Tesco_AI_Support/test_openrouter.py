import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_openrouter():
    api_key = os.getenv("TESCO_AI_SUPPORT_OPENROUTER_MODEL_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://hf.co/spaces/alaselababatunde/Tesco_AI_Support",
        "X-Title": "Tesco AI Support",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {"role": "user", "content": "Hello, are you online?"}
        ]
    }
    
    print(f"Testing OpenRouter with model: {data['model']}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Success!")
        else:
            print(f"Failed with status code {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_openrouter()
