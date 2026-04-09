import os
import fitz  # PyMuPDF
from langchain_core.documents import Document
from src.utils.logger import get_logger
from src.utils.exceptions import DocumentLoadException

logger = get_logger(__name__)


def load_pdfs(data_path: str):
    documents = []

    if not os.path.exists(data_path):
        raise DocumentLoadException(f"Data path does not exist: {data_path}")

    pdf_files = [f for f in os.listdir(data_path) if f.endswith(".pdf")]

    if not pdf_files:
        raise DocumentLoadException("No PDF files found in data directory.")

    for file in pdf_files:
        file_path = os.path.join(data_path, file)

        try:
            logger.info(f"Loading file: {file}")
            pdf = fitz.open(file_path)

            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text = page.get_text().strip()

                # Skip empty or garbage pages
                if not text or len(text) < 50:
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file,
                            "page": page_num + 1
                        }
                    )
                )

        except Exception as e:
            logger.error(f"Failed to process {file}: {str(e)}")
            continue  # skip bad files instead of crashing

    if not documents:
        raise DocumentLoadException("No valid text extracted from PDFs.")

    logger.info(f"Loaded {len(documents)} valid pages from PDFs.")
    return documents