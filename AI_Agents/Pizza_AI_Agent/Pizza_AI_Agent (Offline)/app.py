from flask import Flask, render_template, request, redirect, url_for
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import markdown

app = Flask(__name__)

# Initialize model + prompt
model = OllamaLLM(model="gemma")

template = """
You are an expert in answering questions about Pizza-related topics.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Temporary in-memory history
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_history

    if request.method == "POST":
        question = request.form.get('question', '').strip()
        if question:
            reviews = retriever.invoke(question)
            raw_response = str(chain.invoke({
                "reviews": reviews,
                "question": question
            }))
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
