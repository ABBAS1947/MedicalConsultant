from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHROMA_DIR, EMBEDDING_MODEL
import os


def load_embedding_model():
    """
    Load optimized embedding model for semantic search.
    Uses HuggingFace embeddings for local, fast processing.
    """
    # HuggingFace embeddings (free, local)
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
        encode_kwargs={
            'normalize_embeddings': True,  # Better similarity scores
            'batch_size': 32  # Optimize for speed
        }
    )


def create_vectorstore(documents):
    """
    Create optimized vectorstore with proper indexing.
    """
    embedding_model = load_embedding_model()

    # Create vectorstore with optimized settings
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR,
        collection_name="medical_knowledge_base",
        collection_metadata={
            "hnsw:space": "cosine",  # Cosine similarity for better semantic matching
            "hnsw:construction_ef": 200,  # Higher for better index quality
            "hnsw:M": 48  # Balance between speed and accuracy
        }
    )

    vectordb.persist()
    return vectordb


def load_existing_vectorstore():
    """
    Load an existing vectorstore from disk.
    Returns None if vectorstore doesn't exist.
    """
    if not os.path.exists(CHROMA_DIR) or not os.listdir(CHROMA_DIR):
        return None
    
    embedding_model = load_embedding_model()
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model,
        collection_name="medical_knowledge_base"
    )
    
    return vectordb


def add_documents_to_vectorstore(documents):
    """
    Add new documents to an existing vectorstore.
    Creates vectorstore if it doesn't exist.
    """
    embedding_model = load_embedding_model()
    
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model,
        collection_name="medical_knowledge_base"
    )
    
    vectordb.add_documents(documents)
    vectordb.persist()
    return vectordb
