import os
import fitz  # PyMuPDF
from langchain_core.documents import Document
from uuid import uuid4

from src.utils.logger import get_logger

logger = get_logger(__name__)


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