from flask import Flask, render_template, request, jsonify, make_response
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from vector import retriever
import markdown
import dotenv
import os
import uuid

dotenv.load_dotenv()
app = Flask(__name__)

# OpenRouter LLM Configuration
# Using the secret key name provided by the user
OPENROUTER_API_KEY = os.getenv("DOMINOS_PIZZA_AI_SUPPORT_OPENROUTER_MODEL_KEY")
MODEL_NAME = "openai/gpt-oss-120b:free"

llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://www.dominos.ng/", # Site URL for OpenRouter
        "X-Title": "Domino's Pizza AI Support"
    }
)

# Web Search Tool
search = DuckDuckGoSearchRun()

# System Prompt
SYSTEM_PROMPT = """
You are the official Domino's Pizza AI Support agent for Domino's Pizza Nigeria.
Your goal is to provide exceptional, professional, and friendly assistance to customers.

Guidelines:
1. Always maintain a helpful and appetizing tone.
2. Use Domino's branding and language where appropriate.
3. If you don't know the answer or can't find it in the provided context, state that you'll look it up, and use your web search capabilities (simulated in this flow) to find the most accurate information from https://www.dominos.ng/.
4. Format your responses beautifully using Markdown:
   - Use bold for emphasis.
   - Use lists for steps or menus.
   - Use headers for structure.
5. If the answer involves a logo, mention that more information can be found at the link associated with the Domino's logo.

Context from Domino's Reviews:
{reviews}

User question: {question}
"""

prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

# In-memory chat history per device
chat_sessions = {}

def get_ai_response(question: str, reviews: str) -> str:
    try:
        # First attempt with context
        chain = prompt | llm
        response = chain.invoke({"reviews": reviews, "question": question})
        content = response.content

        # Simple check if AI couldn't answer (heuristics)
        fallback_phrases = ["i don't know", "i am not sure", "i couldn't find", "sorry, i can't"]
        if any(phrase in content.lower() for phrase in fallback_phrases):
             print(f"[INFO] Triggering web search for: {question}")
             search_results = search.run(f"Domino's Pizza Nigeria {question}")
             
             # Re-run with search results
             search_prompt = ChatPromptTemplate.from_template(
                 "The user asked: {question}\n"
                 "I found this information on the web: {search_results}\n"
                 "Provide a final answer as Domino's AI Support using this information."
             )
             search_chain = search_prompt | llm
             response = search_chain.invoke({"question": question, "search_results": search_results})
             content = response.content

        return content
    except Exception as e:
        print(f"[ERROR] AI Response failed: {e}")
        return "I apologize, but I'm having trouble connecting to the pizza ovens (our servers) right now. Please try again in a moment!"

@app.route("/", methods=["GET"])
def index():
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())
    if device_id not in chat_sessions:
        chat_sessions[device_id] = []

    resp = make_response(render_template("index.html", chat_history=chat_sessions[device_id]))
    resp.set_cookie("device_id", device_id)
    return resp

@app.route("/ask", methods=["POST"])
def ask():
    device_id = request.cookies.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())
    if device_id not in chat_sessions:
        chat_sessions[device_id] = []

    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    reviews = str(retriever.invoke(question) or "No specific reviews found.")
    raw_response = get_ai_response(question, reviews)
    
    formatted_response = markdown.markdown(raw_response, extensions=['extra', 'tables'])
    
    chat_sessions[device_id].append({
        "user": question,
        "bot": formatted_response
    })
    return jsonify({"response": formatted_response})

@app.route("/clear", methods=["POST"])
def clear_chat():
    device_id = request.cookies.get("device_id")
    if device_id and device_id in chat_sessions:
        chat_sessions[device_id] = []
    resp = make_response(render_template("index.html", chat_history=[]))
    resp.set_cookie("device_id", device_id)
    return resp
