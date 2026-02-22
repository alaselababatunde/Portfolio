import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RagEngine:
    def __init__(self, data_path="data/tesco_faq.csv", collection_name="tesco_faq"):
        self.data_path = data_path
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # specific embedding function using sentence-transformers
        self.sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.sentence_transformer_ef
        )
        
        # Check if collection is empty, if so, ingest
        if self.collection.count() == 0:
            self.ingest_data()

    def ingest_data(self):
        logger.info(f"Ingesting data from {self.data_path}...")
        try:
            df = pd.read_csv(self.data_path)
            
            documents = []
            metadatas = []
            ids = []
            
            for index, row in df.iterrows():
                # Construct a meaningful document from the row
                # We want the model to see the context: Topic, Subtopic, Question, Answer
                topic = row.get('Topic', '')
                subtopic = row.get('Subtopic', '')
                question = row.get('Question', '')
                answer = row.get('Answer', '')
                
                # Create a rich text representation for embedding
                text_content = f"Topic: {topic}\nSubtopic: {subtopic}\nQuestion: {question}\nAnswer: {answer}"
                
                documents.append(text_content)
                metadatas.append({
                    "topic": str(topic),
                    "subtopic": str(subtopic),
                    "question": str(question)
                })
                ids.append(f"faq_{index}")
            
            # Batch add to avoid potential limits (though 350 is small)
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Successfully ingested {len(documents)} documents.")
            
        except Exception as e:
            logger.error(f"Error ingesting data: {e}")
            raise

    def retrieve(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

if __name__ == "__main__":
    # Test run
    rag = RagEngine()
    results = rag.retrieve("Where do you deliver?")
    print(results)
