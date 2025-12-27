import os
import requests
import gradio as gr
from dotenv import load_dotenv
from vector import VectorStore

load_dotenv()

XAPI_KEY = os.getenv("XAPI_API_KEY")
MODEL = "grok-4-1-fast-reasoning"
XAPI_URL = "https://api.x.ai/v1/chat/completions"

PROJECT_NAME = "OlympiQuery"
ACCENT_COLOR = "#facc15"

vector_store = VectorStore("data/paris-2024-faq.csv")

def stream_xapi(prompt):
    headers = {
        "Authorization": f"Bearer {XAPI_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "stream": True,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a data-focused AI assistant for the Paris 2024 Olympics Fan Dataset. "
                    "Answer strictly using the FAQ context. "
                    "Do not speculate or hallucinate."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    with requests.post(XAPI_URL, headers=headers, json=payload, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data:"):
                    chunk = decoded.replace("data:", "").strip()
                    if chunk == "[DONE]":
                        break
                    try:
                        yield eval(chunk)["choices"][0]["delta"].get("content", "")
                    except:
                        continue

def chat(user_message, history):
    docs = vector_store.search(user_message)
    context = "\n\n".join(docs)

    prompt = f"""
DATASET FAQ CONTEXT:
{context}

USER QUESTION:
{user_message}

Provide a clear, research-oriented answer.
"""

    history.append((user_message, "Analyzing dataset…"))
    yield history, gr.update(visible=False), ""

    response = ""
    for token in stream_xapi(prompt):
        response += token
        history[-1] = (user_message, response)
        yield history, gr.update(visible=False), ""

    sources = "\n\n".join(
        [f"**FAQ Source {i+1}:**\n{d}" for i, d in enumerate(docs)]
    )

    yield history, gr.update(value=sources, visible=True), ""

dark_theme = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="slate",
    font=["Inter", "sans-serif"],
).set(
    body_background_fill="#020617",
    body_text_color="#e5e7eb",
    block_background_fill="#020617",
    block_border_color="#1e293b",
    button_primary_background_fill=ACCENT_COLOR,
    button_primary_text_color="#000000",
)

with gr.Blocks(theme=dark_theme, title=PROJECT_NAME) as demo:

    with gr.Row():
        gr.Image("assets/logo.png", width=60, show_label=False)
        gr.Markdown(
            f"""
            ## {PROJECT_NAME}  
            *AI assistant for the Paris 2024 Olympics Fan Dataset*
            """
        )

    chatbot = gr.Chatbot(height=460, show_label=False)
    sources = gr.Markdown(visible=False)

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Ask about dataset structure, collection methods, insights…",
            show_label=False,
            scale=4,
        )
        send = gr.Button("Ask", scale=1)

    send.click(chat, [user_input, chatbot], [chatbot, sources, user_input])
    user_input.submit(chat, [user_input, chatbot], [chatbot, sources, user_input])

    gr.Markdown(
        "<small>Paris 2024 Dataset • RAG • Grok</small>"
    )

demo.launch(server_port=7860)
