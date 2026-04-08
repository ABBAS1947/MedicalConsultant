from langchain_community.vectorstores import Chroma
from src.utils.logger import get_logger
from src.utils.exceptions import RAGException
from config import CHROMA_DIR, TOP_K, EMBEDDING_MODEL
from src.components.embedding import load_embedding_model

logger = get_logger(__name__)


def load_vectorstore():
    """
    Load existing Chroma vector database.
    """
    try:
        embedding_model = load_embedding_model()

        vectordb = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embedding_model,
            collection_name="medical_knowledge_base"
        )

        logger.info("Vector store loaded successfully.")
        return vectordb

    except Exception as e:
        logger.error(f"Error loading vector store: {str(e)}")
        raise RAGException(str(e))


def get_retriever():
    """
    Create retriever with controlled search parameters.
    """
    vectordb = load_vectorstore()

    retriever = vectordb.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    logger.info(f"Retriever initialized with top_k={TOP_K}")
    return retriever