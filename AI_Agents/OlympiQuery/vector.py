import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, csv_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        df = pd.read_csv(csv_path)

        # Expecting FAQ-style columns
        self.questions = df.iloc[:, 0].astype(str).tolist()
        self.answers = df.iloc[:, 1].astype(str).tolist()

        self.documents = [
            f"FAQ Question:\n{q}\n\nFAQ Answer:\n{a}"
            for q, a in zip(self.questions, self.answers)
        ]

        embeddings = self.model.encode(self.documents)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def search(self, query, k=3):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(np.array(query_embedding), k)
        return [self.documents[i] for i in indices[0]]
