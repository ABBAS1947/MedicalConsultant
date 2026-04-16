#!/usr/bin/env python
"""
Advanced Semantic Search Utilities for Medical Consultant AI
Provides optimized search strategies and evaluation tools.
"""

import os
import time
from typing import List, Dict, Any
from pathlib import Path

from src.components.embedding import load_embedding_model
from src.components.retriever import SemanticRetriever
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SemanticSearchEvaluator:
    """
    Evaluate semantic search quality and performance.
    """

    def __init__(self):
        self.embedding_model = load_embedding_model()
        self.retriever = SemanticRetriever()

    def evaluate_retrieval_quality(self, queries_and_expected_docs: List[Dict[str, Any]]):
        """
        Evaluate retrieval quality using precision, recall, and F1-score.

        Args:
            queries_and_expected_docs: List of dicts with 'query' and 'expected_sources'
        """
        results = []

        for item in queries_and_expected_docs:
            query = item['query']
            expected_sources = set(item['expected_sources'])

            # Retrieve documents
            retrieved_docs = self.retriever.retrieve(query)
            retrieved_sources = set(
                doc.metadata.get('source', '') for doc in retrieved_docs
            )

            # Calculate metrics
            true_positives = len(expected_sources & retrieved_sources)
            false_positives = len(retrieved_sources - expected_sources)
            false_negatives = len(expected_sources - retrieved_sources)

            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            results.append({
                'query': query,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'retrieved_count': len(retrieved_docs)
            })

        return results

    def benchmark_search_speed(self, queries: List[str], num_runs: int = 5):
        """
        Benchmark search speed and latency.

        Args:
            queries: List of test queries
            num_runs: Number of runs for averaging
        """
        latencies = []

        for _ in range(num_runs):
            for query in queries:
                start_time = time.time()
                self.retriever.retrieve(query)
                latency = time.time() - start_time
                latencies.append(latency)

        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0

        return {
            'avg_latency': avg_latency,
            'p95_latency': p95_latency,
            'total_queries': len(queries) * num_runs
        }


def rebuild_vectorstore_with_optimization():
    """
    Rebuild the vectorstore with optimized settings.
    Run this after updating embedding models or chunking strategies.
    """
    from src.components.loader import load_pdfs
    from src.components.cleaner import clean_documents
    from src.components.splitter import split_documents
    from src.components.embedding import create_vectorstore
    from config import DATA_PATH

    logger.info("Rebuilding vectorstore with optimized settings...")

    # Load and process documents
    documents = load_pdfs(DATA_PATH)
    documents = clean_documents(documents)
    split_docs = split_documents(documents)

    # Create optimized vectorstore
    vectorstore = create_vectorstore(split_docs)

    logger.info("Vectorstore rebuilt successfully")
    return vectorstore


if __name__ == "__main__":
    # Example usage
    evaluator = SemanticSearchEvaluator()

    # Test queries for evaluation
    test_data = [
        {
            'query': 'What are the symptoms of hypertension?',
            'expected_sources': ['Medical_book.pdf']
        },
        {
            'query': 'How to treat diabetes?',
            'expected_sources': ['Medical_book.pdf']
        }
    ]

    # Evaluate retrieval quality
    results = evaluator.evaluate_retrieval_quality(test_data)
    for result in results:
        print(f"Query: {result['query']}")
        print(f"F1 Score: {result['f1']:.3f}")
        print("---")

    # Benchmark speed
    benchmark = evaluator.benchmark_search_speed(['test query'] * 10)
    print(f"Average latency: {benchmark['avg_latency']:.3f}s")
    print(f"P95 latency: {benchmark['p95_latency']:.3f}s")