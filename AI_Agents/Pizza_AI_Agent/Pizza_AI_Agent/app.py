from flask import Flask, render_template, request, redirect, url_for
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import markdown
import dotenv
from openai import OpenAI
import os


dotenv.load_dotenv()
app = Flask(__name__)



api_key = os.getenv("OPENROUTER_API_KEY")
print("DEBUG: OPENROUTER_API_KEY=", repr(api_key))  # Debug print
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment or .env file.")


import requests

# Custom OpenAI client with Bearer token in Authorization header
class OpenRouterOpenAI(OpenAI):
    def __init__(self, base_url, api_key):
        super().__init__(base_url=base_url, api_key=api_key)
        self.base_url = base_url
        self.api_key = api_key

    def chat_completion(self, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://openrouter.ai/docs/quickstart",  # Optional, for analytics
            "X-Title": "Pizza AI Agent",  # Optional, for analytics
        }
        # Ensure no double slash in URL
        url = str(self.base_url).rstrip("/") + "/chat/completions"
        response = requests.post(url, headers=headers, json=kwargs)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("OpenRouter API error:", response.status_code, response.text)
            raise
        return response.json()

client = OpenRouterOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


template = """
You are an expert in answering questions about Pizza-related topics.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

# Use OpenAI client directly for completions
def run_chain(reviews, question):
    prompt_text = prompt.format(reviews=reviews, question=question)
    payload = {
        "model": "mistralai/mistral-nemo:free",
        "messages": [
            {"role": "system", "content": "You are an expert in answering questions about Pizza-related topics."},
            {"role": "user", "content": prompt_text}
        ]
    }
    response = client.chat_completion(**payload)
    return response["choices"][0]["message"]["content"]

# Temporary in-memory history
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history

    if request.method == "POST":
        question = request.form.get('question', '').strip()
        if question:
            reviews = retriever.invoke(question)
            raw_response = run_chain(reviews, question)
            response_html = markdown.markdown(raw_response)

            # Save to history
            chat_history.append({
                "user": question,
                "bot": response_html
            })
        return redirect(url_for('index'))  # Redirect to avoid form re-submission

    return render_template('index.html', chat_history=chat_history)

@app.route('/clear', methods=['POST'])
def clear_chat():
    global chat_history
    chat_history = []
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
