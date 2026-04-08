import os
import fitz  # PyMuPDF
from typing import List, Dict
from src.utils.logger import get_logger
from src.utils.exceptions import RAGException

logger = get_logger(__name__)


def load_pdfs(data_path: str) -> List[Dict]:
    """
    Load all PDF documents from a directory using PyMuPDF.

    Returns:
        List of dicts with keys: text, source, page
    """
    if not os.path.exists(data_path):
        raise RAGException(f"Data path does not exist: {data_path}")

    documents = []

    try:
        for file_name in os.listdir(data_path):
            if not file_name.lower().endswith(".pdf"):
                continue

            file_path = os.path.join(data_path, file_name)
            logger.info(f"Loading file: {file_name}")

            pdf = fitz.open(file_path)

            for page_num, page in enumerate(pdf):
                text = page.get_text("text")

                if text and text.strip():
                    documents.append({
                        "text": text.strip(),
                        "source": file_name,
                        "page": page_num + 1
                    })

            pdf.close()

        if not documents:
            raise RAGException("No valid text extracted from PDFs.")

        logger.info(f"Loaded {len(documents)} pages from PDFs.")
        return documents

    except Exception as e:
        logger.error(f"Error loading PDFs: {str(e)}")
        raise RAGException(str(e))