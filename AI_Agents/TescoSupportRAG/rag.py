import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class TescoRAG:
    def __init__(self, csv_path: str):
        # Safe CSV loading (prevents tokenizing errors)
        df = pd.read_csv(csv_path, engine="python")

        # Enforce exactly two columns
        df = df.iloc[:, :2]
        df.columns = ["question", "answer"]

        # Clean data
        df.dropna(inplace=True)

        self.questions = df["question"].astype(str).tolist()
        self.answers = df["answer"].astype(str).tolist()

        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self.model.encode(
            self.questions,
            normalize_embeddings=True
        )

    def query(self, user_question: str) -> str:
        query_embedding = self.model.encode(
            [user_question],
            normalize_embeddings=True
        )

        scores = cosine_similarity(query_embedding, self.embeddings)[0]
        best_index = int(np.argmax(scores))

        return self.answers[best_index]
