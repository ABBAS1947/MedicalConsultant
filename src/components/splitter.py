from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.logger import get_logger
from src.utils.exceptions import ChunkingException

logger = get_logger(__name__)


def split_documents(documents):
    if not documents:
        raise ChunkingException("No documents provided for splitting.")

    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        chunks = splitter.split_documents(documents)

        # Filter bad chunks
        clean_chunks = [
            chunk for chunk in chunks
            if chunk.page_content and len(chunk.page_content.strip()) > 30
        ]

        logger.info(f"Created {len(clean_chunks)} clean chunks from {len(documents)} documents.")

        if not clean_chunks:
            raise ChunkingException("Chunking resulted in zero valid chunks.")

        return clean_chunks

    except Exception as e:
        logger.error(f"Chunking failed: {str(e)}")
        raise ChunkingException(str(e))