# 🌾 AgriCopilot AI Backend

**AgriCopilot** is a multilingual AI assistant designed to support farmers through intelligent diagnostics, multilingual chat, agricultural disaster response, and marketplace recommendations.  
It integrates Hugging Face conversational models with FastAPI to deliver real-time, context-aware, and multilingual support for farmers across the world.  

---

## 🚀 Features

- 🧠 **AI Crop Doctor** — Diagnose crop diseases and get treatment advice.  
- 💬 **Multilingual Farmer Chat** — Speak with the AI in your preferred language.  
- 🌦 **Disaster Response Summarizer** — Simplifies agricultural disaster reports into actionable steps.  
- 🛒 **Marketplace Recommender** — Helps farmers buy or sell produce with smart recommendations.  
- 🔍 **Vector Search Integration** — Enables context-aware search powered by embeddings.  
- 🔐 **Bearer Token Security** — Protects endpoints using a configurable API key.  

---

## 🧩 Tech Stack

- **Backend Framework:** FastAPI  
- **AI Models:** Hugging Face (Meta-Llama 3.x)  
- **Prompt Management:** LangChain + HuggingFaceEndpoint  
- **Embeddings / Search:** Vector similarity (via `vector.py`)  
- **Deployment:** Docker / Hugging Face Spaces  
- **Authentication:** Bearer Token (`agricopilot404` by default)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/agricopilot-backend.git
cd agricopilot-backend

