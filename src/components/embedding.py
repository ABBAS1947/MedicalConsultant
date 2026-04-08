from langchain.embeddings import HuggingFaceEmbeddings
from src.utils.logger import get_logger
from config import EMBEDDING_MODEL

logger = get_logger(__name__)


def load_embedding_model():
    """
    Load embedding model locally.
    """
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )