import os
from typing import List, Dict


def validate_directory(path: str):
    """
    Ensure directory exists, create if not.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def format_sources(docs: List[Dict]) -> List[str]:
    """
    Format source metadata for display.
    """
    formatted = []

    for doc in docs:
        source = doc.get("source", "Unknown")
        page = doc.get("page", "N/A")
        formatted.append(f"{source} (Page {page})")

    return formatted