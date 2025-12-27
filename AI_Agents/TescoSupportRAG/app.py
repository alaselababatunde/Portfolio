import gradio as gr
from rag import TescoRAG

# Initialize RAG system
rag = TescoRAG("data/tesco_online_grocery_faq.csv")


def chat(user_input):
    if not user_input.strip():
        return "Please ask a valid question."
    return rag.query(user_input)


demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(
        label="Ask a Tesco Online Grocery question",
        placeholder="e.g. How do I amend my grocery order?"
    ),
    outputs=gr.Textbox(label="Answer"),
    title="TescoSupportRAG",
    description="A Retrieval-Augmented FAQ assistant trained on Tesco Online Grocery FAQs."
)

if __name__ == "__main__":
    demo.launch()
