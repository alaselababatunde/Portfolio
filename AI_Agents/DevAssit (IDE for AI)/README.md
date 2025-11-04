# 🧠 DevAssist AI — Developer-Centric Code Intelligence System

**DevAssist AI** is an advanced coding assistant built under **Alash Studios**, designed to help developers generate, document, and refine production-ready code using modern AI models and retrieval systems.  
It combines **Hugging Face**, **LangChain**, and **FastAPI** into one scalable backend ecosystem for intelligent code automation.

---

## 🚀 Overview

DevAssist AI assists developers in:
- Writing and refactoring production-level code.
- Generating professional documentation automatically.
- Building front-end SME (Subject Matter Expert) sites from prompts.
- Supporting multi-modal input (text + speech).
- Retrieving context-aware examples through vector search.

---

## ⚙️ System Architecture

**Architecture Summary:**
- **Frontend:** Web-based interface (HTML, CSS, JS)
- **Backend:** FastAPI + Uvicorn ASGI Server
- **Model Hosting:** Hugging Face Spaces
- **Vector Database:** ChromaDB
- **Embeddings:** `intfloat/e5-large-v2`
- **LLM Models:** StarCoder, DeepSeek, and CodeGen pipelines
- **Audio AI:** Spitch API for speech-to-text and translation

**Architecture Layers:**
1. **Chat Layer:** Conversational coding assistant.
2. **Code Layer:** Documentation and SME site generator.
3. **Retrieval Layer:** Vector search + contextual augmentation.
4. **Speech Layer:** Converts developer speech into prompts for code generation.

---

## 🧩 Tools and Dependencies

| **Tool / Library** | **Purpose** | **Plan / Cost** |
|---------------------|-------------|-----------------|
| **Hugging Face Spaces** | Model hosting & deployment | Free → *Pro $20/mo* |
| **Hugging Face Transformers** | Model inference (LLMs) | Free |
| **LangChain** | Chaining & contextual workflows | Free |
| **LangChain-Chroma** | Vector database integration | Free |
| **FastAPI** | Backend API framework | Free |
| **Spitch** | Speech-to-text & translation | Pay-as-you-go |
| **Pandas** | Data processing | Free |
| **Python-Multipart** | File upload handling | Free |
| **Uvicorn** | ASGI server | Free |
| **Sentence-Transformers** | Embedding model backend | Free |

---

## 💾 Vector Database Setup

**Vector Engine:** ChromaDB  
**Dataset File:** `sme_builder_dataset.csv`  
**Embedding Model:** `intfloat/e5-large-v2`  

The retriever indexes the dataset to provide contextual data for front-end generation tasks.  
Each document includes code samples, sector information, and HTML/CSS/JS references to improve generation accuracy.

---

## 🧠 Model Architecture

**Current Models:**
- `deepseek-ai/deepseek-coder-1.3b-instruct` — front-end generation
- `bigcode/starcoderbase` — code completion & explanation
- `Salesforce/codegen-2B-mono` — auto documentation
- `intfloat/e5-large-v2` — semantic embedding model

**Pipeline Flow:**
1. User sends prompt or speech input.
2. Context is retrieved via vector search.
3. Input and context are chained into the prompt.
4. The LLM generates output → returned via API as JSON.

---

## 🔐 Authentication

All routes are protected via Bearer Token.

**Example Header:**
```http
Authorization: Bearer super-secret-123

