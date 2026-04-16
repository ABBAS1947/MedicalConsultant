import os
import fitz  # PyMuPDF
from langchain_core.documents import Document
from uuid import uuid4
import json

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Metadata file to track processed PDFs
PROCESSED_FILES_METADATA = ".processed_files.json"


def get_processed_files() -> set:
    """
    Get set of already processed PDF filenames.
    """
    if os.path.exists(PROCESSED_FILES_METADATA):
        try:
            with open(PROCESSED_FILES_METADATA, 'r') as f:
                data = json.load(f)
                return set(data.get("processed_files", []))
        except Exception as e:
            logger.warning(f"Failed to load processed files metadata: {e}")
            return set()
    return set()


def save_processed_files(filenames: list):
    """
    Save the list of processed PDF filenames.
    """
    try:
        data = {
            "processed_files": sorted(filenames)
        }
        with open(PROCESSED_FILES_METADATA, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved processed files metadata: {len(filenames)} files")
    except Exception as e:
        logger.error(f"Failed to save processed files metadata: {e}")


def get_new_pdf_files(data_path: str) -> tuple[list, set]:
    """
    Get list of new PDF files that haven't been processed yet.
    Returns (new_files, all_files_set)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data path not found: {data_path}")

    all_pdf_files = [f for f in os.listdir(data_path) if f.lower().endswith(".pdf")]
    processed_files = get_processed_files()
    
    new_files = [f for f in all_pdf_files if f not in processed_files]
    
    logger.info(f"Total PDFs in directory: {len(all_pdf_files)}")
    logger.info(f"Already processed: {len(processed_files)}")
    logger.info(f"New files to process: {len(new_files)}")
    
    return new_files, set(all_pdf_files)


def load_pdfs(data_path: str):
    documents = []

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data path not found: {data_path}")

    pdf_files = [f for f in os.listdir(data_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        raise ValueError("No PDF files found in data directory.")

    total_pages = 0
    skipped_pages = 0

    for file in pdf_files:
        file_path = os.path.join(data_path, file)

        try:
            logger.info(f"Processing file: {file}")
            pdf = fitz.open(file_path)

            for page_num in range(len(pdf)):
                try:
                    page = pdf[page_num]
                    text = page.get_text()

                    total_pages += 1

                    if not text or len(text.strip()) < 50:
                        skipped_pages += 1
                        continue

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file,
                                "page": page_num + 1,
                                "doc_id": str(uuid4())
                            }
                        )
                    )

                except Exception as page_error:
                    logger.warning(f"Skipped page {page_num+1} in {file}: {page_error}")
                    skipped_pages += 1
                    continue

        except Exception as file_error:
            logger.error(f"Failed file {file}: {file_error}")
            continue

    logger.info(f"Total pages processed: {total_pages}")
    logger.info(f"Skipped pages: {skipped_pages}")
    logger.info(f"Valid documents: {len(documents)}")

    if not documents:
        raise ValueError("No valid content extracted from PDFs.")

    return documents


def load_new_pdfs(data_path: str):
    """
    Load only new PDF files that haven't been processed yet.
    Returns (documents, all_pdf_filenames_set)
    """
    documents = []
    
    new_files, all_files = get_new_pdf_files(data_path)
    
    if not new_files:
        logger.info("No new PDF files to process.")
        return documents, all_files

    total_pages = 0
    skipped_pages = 0

    for file in new_files:
        file_path = os.path.join(data_path, file)

        try:
            logger.info(f"Processing new file: {file}")
            pdf = fitz.open(file_path)

            for page_num in range(len(pdf)):
                try:
                    page = pdf[page_num]
                    text = page.get_text()

                    total_pages += 1

                    if not text or len(text.strip()) < 50:
                        skipped_pages += 1
                        continue

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": file,
                                "page": page_num + 1,
                                "doc_id": str(uuid4())
                            }
                        )
                    )

                except Exception as page_error:
                    logger.warning(f"Skipped page {page_num+1} in {file}: {page_error}")
                    skipped_pages += 1
                    continue

        except Exception as file_error:
            logger.error(f"Failed processing new file {file}: {file_error}")
            continue

    logger.info(f"New files - Total pages: {total_pages}, Skipped: {skipped_pages}, Valid docs: {len(documents)}")
    
    return documents, all_files