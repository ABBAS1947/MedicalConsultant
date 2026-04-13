from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from src.utils.logger import get_logger

logger = get_logger(__name__)


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Enterprise-grade document splitter.

    Features:
    - Recursive splitting (structure-aware)
    - Configurable chunk size & overlap
    - Metadata preservation
    - Unique chunk IDs
    """

    logger.info("Starting document splitting...")

    # 🔧 CONFIG (tune later if needed)
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",  # paragraphs
            "\n",    # lines
            ". ",    # sentences
            " ",     # words
            ""       # characters fallback
        ]
    )

    chunks = []
    chunk_id = 0

    for doc in documents:
        split_docs = splitter.split_documents([doc])

        for chunk in split_docs:
            # 🧠 Add metadata
            chunk.metadata["chunk_id"] = chunk_id
            chunk.metadata["source"] = doc.metadata.get("source", "unknown")
            chunk.metadata["page"] = doc.metadata.get("page", "unknown")

            chunks.append(chunk)
            chunk_id += 1

    logger.info(f"Splitting completed. Total chunks: {len(chunks)}")

    return chunks