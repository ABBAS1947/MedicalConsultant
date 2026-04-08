class RAGException(Exception):
    """
    Base exception for RAG system.
    """
    def __init__(self, message: str):
        super().__init__(message)


class DocumentLoadException(RAGException):
    pass


class ChunkingException(RAGException):
    pass


class VectorStoreException(RAGException):
    pass


class RetrievalException(RAGException):
    pass