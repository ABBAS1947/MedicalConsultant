import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

CHROMA_DIR = os.getenv("CHROMA_DIR", "vectorstore")
DATA_PATH = os.getenv("DATA_PATH", "data/raw")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3