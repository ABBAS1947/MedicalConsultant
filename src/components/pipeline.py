import os

from src.components.loader import load_pdfs
from src.components.cleaner import clean_documents
from src.components.splitter import split_documents
from src.components.embedding import load_embedding_model
from src.components.embedding import create_vectorstore

from src.utils.logger import get_logger
from config import DATA_PATH, CHROMA_DIR

logger = get_logger(__name__)


def run_ingestion_pipeline():
    """
    Full ingestion pipeline:
    - Load documents
    - Clean text
    - Split into chunks
    - Create embeddings
    - Store in vector DB
    """

    # Skip if already exists
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        logger.info("Vector store already exists. Skipping ingestion.")
        return

    logger.info("Starting ingestion pipeline...")

    # Step 1: Load
    documents = load_pdfs(DATA_PATH)

    # Step 2: Clean (NEW - critical)
    documents = clean_documents(documents)

    if not documents:
        raise ValueError("No valid documents after cleaning.")

    # Step 3: Split
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("Chunking resulted in zero chunks.")

    # Step 4: Embeddings
    embedding_model = load_embedding_model()

    # Step 5: Vector store
    create_vectorstore(chunks)

    logger.info(f"Final stats → Documents: {len(documents)}, Chunks: {len(chunks)}")
    logger.info("Ingestion pipeline completed successfully.")