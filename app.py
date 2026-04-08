from src.components.pipeline import run_ingestion_pipeline
from src.components.retriever import get_retriever
from src.components.rag_chain import RAGChain


def main():
    # Step 1: Ensure data is ingested
    run_ingestion_pipeline()

    # Step 2: Load retriever
    retriever = get_retriever()

    # Step 3: Initialize RAG system
    rag = RAGChain(retriever)

    # Step 4: CLI loop
    while True:
        query = input("\nAsk (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        result = rag.generate_response(query)

        print("\nAnswer:\n", result["answer"])
        print("\nSources:")
        for src in result["sources"]:
            print(f"- {src['source']} (Page {src['page']})")


if __name__ == "__main__":
    main()