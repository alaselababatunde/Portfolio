import os
import pandas as pd
import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ==============================
# Logging Setup
# ==============================
logger = logging.getLogger("DevAssist.Vector")
logging.basicConfig(level=logging.INFO)

# ==============================
# Configuration
# ==============================
DATASET_PATH = os.getenv("SME_DATASET_PATH", "sme_builder_dataset.csv")
DB_LOCATION = os.getenv("CHROMA_DB_DIR", "./DevAssist_SME_Builder_DB")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "landing_page_generation_examples")
EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "intfloat/e5-large-v2")
HF_CACHE_DIR = os.getenv("HF_HOME", "/app/huggingface_cache")

os.makedirs(HF_CACHE_DIR, exist_ok=True)
os.makedirs(DB_LOCATION, exist_ok=True)

# ==============================
# Validate Dataset
# ==============================
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"❌ Dataset not found: {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)
if df.empty:
    raise ValueError("❌ SME dataset is empty — cannot initialize vector DB.")

# ==============================
# Embedding Model
# ==============================
try:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    logger.info(f"✅ Embedding model loaded: {EMBEDDING_MODEL}")
except Exception as e:
    raise RuntimeError(f"⚠️ Failed to load embedding model: {e}")

# ==============================
# Initialize Vector Store
# ==============================
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings,
)

# Only add documents if DB is new or empty
if not os.listdir(DB_LOCATION):
    logger.info("🧩 Initializing new Chroma vector store from dataset...")
    documents = []
    for i, row in df.iterrows():
        content_parts = [
            str(row.get("prompt", "")),
            str(row.get("html_code", "")),
            str(row.get("css_code", "")),
            str(row.get("js_code", "")),
            str(row.get("sector", "")),
        ]
        content = " ".join([p for p in content_parts if p.strip()])
        if not content.strip():
            continue
        documents.append(Document(page_content=content, metadata={"id": str(i)}))

    if documents:
        vector_store.add_documents(documents=documents)
        logger.info(f"✅ Added {len(documents)} documents to Chroma DB.")
    else:
        logger.warning("⚠️ No valid documents found in dataset to embed.")
else:
    logger.info("💾 Using existing Chroma vector store (no rebuild).")

# ==============================
# Retriever
# ==============================
retriever = vector_store.as_retriever(search_kwargs={"k": 20})
logger.info(
    f"SME vector store ready → collection='{COLLECTION_NAME}', "
    f"docs={vector_store._collection.count()}"
)
