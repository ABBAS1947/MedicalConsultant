from langchain_community.vectorstores import Chroma
from src.utils.logger import get_logger
from src.utils.exceptions import RAGException
from config import (
    CHROMA_DIR, TOP_K, EMBEDDING_MODEL, SEARCH_TYPE, SEARCH_KWARGS, RERANK_TOP_K
)
from src.components.embedding import load_embedding_model

logger = get_logger(__name__)


class SemanticRetriever:
    """
    Advanced semantic retriever with MMR search for better diversity and relevance.
    """

    def __init__(self):
        self.embedding_model = load_embedding_model()
        self.vectorstore = self._load_vectorstore()

    def _load_vectorstore(self):
        """Load existing Chroma vector database."""
        try:
            vectordb = Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=self.embedding_model,
                collection_name="medical_knowledge_base"
            )
            logger.info("Vector store loaded successfully.")
            return vectordb
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise RAGException(str(e))

    def retrieve(self, query, top_k=None):
        """
        Perform advanced semantic search using MMR for optimal relevance-diversity balance.

        Args:
            query: Search query string
            top_k: Number of results to return (default: RERANK_TOP_K)

        Returns:
            List of relevant documents
        """
        if top_k is None:
            top_k = RERANK_TOP_K

        try:
            # Use MMR (Maximal Marginal Relevance) for better search quality
            retriever = self.vectorstore.as_retriever(
                search_type=SEARCH_TYPE,
                search_kwargs=SEARCH_KWARGS
            )

            docs = retriever.invoke(query)

            logger.info(f"Retrieved {len(docs)} documents using {SEARCH_TYPE} search for query: {query[:50]}...")
            return docs[:top_k]

        except Exception as e:
            logger.error(f"Advanced retrieval error: {str(e)}")
            # Fallback to basic similarity search
            try:
                docs = self.vectorstore.similarity_search(query, k=top_k)
                return docs
            except Exception as fallback_e:
                logger.error(f"Fallback retrieval failed: {str(fallback_e)}")
                return []


def get_retriever():
    """
    Factory function to create the advanced semantic retriever.
    """
    return SemanticRetriever()