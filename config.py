import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

CHROMA_DIR = os.getenv("CHROMA_DIR", "vectorstore")
DATA_PATH = os.getenv("DATA_PATH", "data/raw")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5  # Increased for better retrieval
RERANK_TOP_K = 3  # Final results after reranking

# Semantic search configuration
SEARCH_TYPE = "mmr"  # Options: similarity, mmr, similarity_score_threshold
SEARCH_KWARGS = {
    "k": TOP_K,
    "fetch_k": 20,  # Fetch more for MMR diversity
    "lambda_mult": 0.5,  # Balance relevance vs diversity
    "score_threshold": 0.7  # Minimum similarity score
}

# Hybrid search (if using Chroma with keyword support)
USE_HYBRID_SEARCH = True
KEYWORD_WEIGHT = 0.3
SEMANTIC_WEIGHT = 0.7