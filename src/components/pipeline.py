import os
from src.components.loader import load_pdfs
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
    - Split into chunks
    - Create embeddings
    - Store in vector DB
    """

    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        logger.info("Vector store already exists. Skipping ingestion.")
        return

    logger.info("Starting ingestion pipeline...")

    documents = load_pdfs(DATA_PATH)
    chunks = split_documents(documents)
    embedding_model = load_embedding_model()

    create_vectorstore(chunks)

    logger.info("Ingestion pipeline completed successfully.")