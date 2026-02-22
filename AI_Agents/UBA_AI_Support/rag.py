import os
import glob
from typing import List, Dict, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DATA_DIR = "./data"
CHROMA_DIR = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class RAGSystem:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.vectorstore = None
        self._initialize_db()

    def _initialize_db(self):
        """Initializes or loads the ChromaDB with data from DATA_DIR."""
        if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
            print("Initializing new vector database from PDFs...")
            pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
            all_docs = []
            
            for pdf in pdf_files:
                try:
                    loader = PyPDFLoader(pdf)
                    docs = loader.load()
                    all_docs.extend(docs)
                except Exception as e:
                    print(f"Error loading {pdf}: {e}")
            
            if all_docs:
                splits = self.text_splitter.split_documents(all_docs)
                self.vectorstore = Chroma.from_documents(
                    documents=splits,
                    embedding=self.embeddings,
                    persist_directory=CHROMA_DIR
                )
                print(f"Indexed {len(splits)} chunks.")
            else:
                self.vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=self.embeddings)
        else:
            print("Loading existing vector database...")
            self.vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=self.embeddings)

    def query(self, text: str, k: int = 5) -> str:
        """Queries the vector database and returns a combined context string."""
        if not self.vectorstore:
            return ""
        
        results = self.vectorstore.similarity_search(text, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context

# Singleton instance
rag_system = RAGSystem()
