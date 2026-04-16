from langchain_ollama import OllamaLLM
from src.utils.prompt import SYSTEM_PROMPT
from src.utils.logger import get_logger
from config import MODEL_NAME, RERANK_TOP_K

logger = get_logger(__name__)


class RAGChain:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = OllamaLLM(
            model=MODEL_NAME,
            base_url="http://localhost:11434",
            temperature=0.2
        )

    def generate_response(self, query: str):
        try:
            docs = self.retriever.retrieve(query, top_k=RERANK_TOP_K)

            if not docs:
                return {
                    "answer": "I don't know",
                    "sources": []
                }

            context = "\n\n".join([doc.page_content for doc in docs])

            # Limit context length to prevent LLM timeout
            max_context_length = 4000  # characters
            if len(context) > max_context_length:
                context = context[:max_context_length] + "..."

            prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}

Answer:
"""

            response = self.llm.invoke(prompt)

            sources = [
                {
                    "source": doc.metadata.get("source"),
                    "page": doc.metadata.get("page")
                }
                for doc in docs
            ]

            return {
                "answer": response,
                "sources": sources
            }

        except Exception as e:
            logger.error(f"RAG error: {str(e)}")
            return {
                "answer": "An error occurred while processing the query.",
                "sources": []
            }