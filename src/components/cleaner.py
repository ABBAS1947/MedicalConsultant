import re
from src.utils.logger import get_logger

logger = get_logger(__name__)


def clean_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)

    # Remove page numbers
    text = re.sub(r'(?i)page\s*\d+', '', text)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # Remove common headers/footers
    text = re.sub(r'(?i)chapter\s+\d+.*', '', text)
    text = re.sub(r'(?i)copyright.*', '', text)

    # Clean spaces
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


def clean_documents(documents):
    cleaned_docs = []
    removed = 0

    for doc in documents:
        cleaned = clean_text(doc.page_content)

        if not cleaned or len(cleaned) < 50:
            removed += 1
            continue

        doc.page_content = cleaned
        cleaned_docs.append(doc)

    logger.info(f"Cleaned documents: {len(cleaned_docs)}")
    logger.info(f"Removed noisy documents: {removed}")

    return cleaned_docs