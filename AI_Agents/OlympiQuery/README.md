---
title: HelpDeskRAG
emoji: ⚡
colorFrom: red
colorTo: green
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Retrieval-Augmented Customer Support Assistant
---

# OlympiQuery 🏅

OlympiQuery is an AI-powered assistant designed to help users explore and understand
the **Paris 2024 Olympics Fan Dataset** through natural language questions.

It uses Retrieval-Augmented Generation (RAG) to answer queries strictly based on
the official FAQ data, ensuring accurate and trustworthy responses.

## Features
- Dataset-aware question answering
- FAQ-based retrieval (FAISS)
- Grok reasoning model via xAPI
- Streaming responses
- Source citations
- Dark-mode optimized UI

## Dataset
The assistant is powered by the Paris 2024 Fan Dataset FAQ, covering:
- Fan engagement
- Demographics
- Ticket sales
- Event attendance
- Data collection methods
- Dataset structure and usage

## Usage
Ask questions such as:
- How was the data collected?
- What insights can be derived from ticket sales?
- What does the dataset include?

## Deployment
Built for Hugging Face Spaces  
Runs on port **7860**
