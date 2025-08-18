from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# --- Embedding and Vector Store Setup ---
df = pd.read_csv("realistic_restaurant_reviews.csv")

# Use sentence-transformers/all-MiniLM-L6-v2 (or other good models)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db_location = "./Pizza_AI_Agent_DB"
add_documents = not os.path.exists(db_location)

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

vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
