import os
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# --- Embedding and Vector Store Setup ---

# Ensure writable directory for Chroma DB inside the container
db_location = "/app/Pizza_AI_Agent_DB"
os.makedirs(db_location, exist_ok=True)

# Load your CSV dataset
df = pd.read_csv("realistic_restaurant_reviews.csv")

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"trust_remote_code": True}
)

# Determine if we need to add documents
add_documents = not os.listdir(db_location)  # empty directory = add documents

# Prepare documents
if add_documents:
    documents = []
    ids = []
    for i, row in df.iterrows():
        title = str(row.get("Title", ""))
        review = str(row.get("Review", ""))
        page_content = (title + ". " + review).strip()
        metadata = {}
        if "Rating" in row:
            metadata["rating"] = row["Rating"]
        if "Date" in row:
            metadata["date"] = row["Date"]
        document = Document(
            page_content=page_content,
            metadata=metadata,
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

# Initialize Chroma vector store
vector_store = Chroma(
    persist_directory=db_location,
    collection_name="restaurant_reviews",
    embedding_function=embeddings
)

# Add documents if directory was empty
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
