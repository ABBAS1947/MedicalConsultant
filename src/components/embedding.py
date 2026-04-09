from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHROMA_DIR, EMBEDDING_MODEL


def load_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


def create_vectorstore(documents):
    embedding_model = load_embedding_model()

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR,
        collection_name="medical_knowledge_base"
    )

    vectordb.persist()
    return vectordb
