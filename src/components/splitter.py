from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.logger import get_logger
from src.utils.exceptions import RAGException
from config import CHUNK_SIZE, CHUNK_OVERLAP

logger = get_logger(__name__)


def split_documents(documents: List[Dict]) -> List[Dict]:
    """
    Split documents into chunks while preserving metadata.
    """
    if not documents:
        raise RAGException("No documents provided for splitting.")

    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        chunks = []

        for doc in documents:
            split_texts = splitter.split_text(doc["text"])

            for chunk in split_texts:
                if chunk.strip():
                    chunks.append({
                        "text": chunk.strip(),
                        "source": doc["source"],
                        "page": doc["page"]
                    })

        if not chunks:
            raise RAGException("Chunking failed. No chunks created.")

        logger.info(f"Created {len(chunks)} chunks.")
        return chunks

    except Exception as e:
        logger.error(f"Error during splitting: {str(e)}")
        raise RAGException(str(e))