import os

from src.components.loader import load_pdfs, load_new_pdfs, save_processed_files, get_processed_files
from src.components.cleaner import clean_documents
from src.components.splitter import split_documents
from src.components.embedding import load_embedding_model
from src.components.embedding import create_vectorstore, load_existing_vectorstore, add_documents_to_vectorstore

from src.utils.logger import get_logger
from config import DATA_PATH, CHROMA_DIR

logger = get_logger(__name__)


def run_ingestion_pipeline():
    """
    Full ingestion pipeline with incremental document processing:
    - Load NEW documents (skip already processed)
    - Clean text
    - Split into chunks
    - Create or update embeddings in vector DB
    
    Supports adding new PDFs without rebuilding entire vector store.
    """

    logger.info("="*50)
    logger.info("Starting ingestion pipeline...")
    logger.info("="*50)

    vectorstore_exists = os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR)

    if vectorstore_exists:
        # INCREMENTAL MODE: Add new documents to existing vectorstore
        logger.info("Vector store exists. Running in INCREMENTAL mode...")
        
        try:
            # Step 1: Load only new PDFs
            documents, all_files = load_new_pdfs(DATA_PATH)
            
            if not documents:
                logger.info("✓ No new documents to process. Vector store is up to date.")
                return
            
            logger.info(f"Found {len(documents)} new documents to add.")
            
            # Step 2: Clean
            documents = clean_documents(documents)
            
            if not documents:
                logger.warning("No valid documents after cleaning.")
                return
            
            # Step 3: Split
            chunks = split_documents(documents)
            
            if not chunks:
                logger.warning("Chunking resulted in zero chunks.")
                return
            
            # Step 4: Add to existing vectorstore
            add_documents_to_vectorstore(chunks)
            
            # Step 5: Update processed files tracking
            save_processed_files(list(all_files))
            
            logger.info(f"✓ Incremental ingestion complete! Added {len(documents)} documents ({len(chunks)} chunks)")
            logger.info("="*50)
            
        except Exception as e:
            logger.error(f"Error in incremental ingestion: {e}", exc_info=True)
            raise
    
    else:
        # INITIAL MODE: Create new vectorstore with all documents
        logger.info("Vector store doesn't exist. Running in INITIAL mode...")
        
        try:
            # Step 1: Load all PDFs
            documents = load_pdfs(DATA_PATH)
            logger.info(f"Loaded {len(documents)} documents from PDFs")
            
            # Step 2: Clean (critical)
            documents = clean_documents(documents)
            
            if not documents:
                raise ValueError("No valid documents after cleaning.")
            
            # Step 3: Split
            chunks = split_documents(documents)
            
            if not chunks:
                raise ValueError("Chunking resulted in zero chunks.")
            
            # Step 4: Embeddings & create vectorstore
            embedding_model = load_embedding_model()
            create_vectorstore(chunks)
            
            # Step 5: Save processed files tracking
            # Get all PDF filenames from data directory
            all_pdf_files = [f for f in os.listdir(DATA_PATH) if f.lower().endswith(".pdf")]
            save_processed_files(all_pdf_files)
            
            logger.info(f"✓ Initial ingestion complete! Processed {len(documents)} documents ({len(chunks)} chunks)")
            logger.info("="*50)
            
        except Exception as e:
            logger.error(f"Error in initial ingestion: {e}", exc_info=True)
            raise