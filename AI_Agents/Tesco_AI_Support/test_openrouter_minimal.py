import json
import urllib.request
import urllib.error
import socket

def test_model(model_id):
    api_key = "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"
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://hf.co/spaces/alaselababatunde/Tesco_AI_Support",
        "X-Title": "Tesco AI Support",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "Hello, are you online?"}
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
    
    print(f"\n--- Testing Model: {model_id} ---")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode()
            print(f"Status: {response.status}")
            print(f"Response snippet: {res_body[:200]}...")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
    except socket.timeout:
        print("Error: Request timed out")
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    models = [
        "openai/gpt-oss-120b:free",
        "google/gemma-7b-it:free",
        "mistralai/mistral-7b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free"
    ]
    
    for model in models:
        if test_model(model):
            print(f"\nSUCCESS with {model}")
            break
