from pathlib import Path
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import logging

from src.components.pipeline import run_ingestion_pipeline
from src.components.retriever import get_retriever
from src.components.rag_chain import RAGChain
from src.utils.logger import get_logger

# Initialize FastAPI app
app = FastAPI(
    title="Medical Consultant API",
    description="RAG-based Medical Consultation API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger(__name__)

# Pydantic models
class QueryRequest(BaseModel):
    query: str

class SourceMetadata(BaseModel):
    source: Optional[str]
    page: Optional[int]

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceMetadata]
    query: str

class HealthResponse(BaseModel):
    status: str
    message: str

# Global RAG instance
rag_chain = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_chain
    try:
        logger.info("Initializing RAG system...")
        run_ingestion_pipeline()
        retriever = get_retriever()
        rag_chain = RAGChain(retriever)
        logger.info("RAG system initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        raise

@app.get("/", response_class=FileResponse)
async def root():
    """Serve the frontend application"""
    index_path = Path(__file__).resolve().parent / "index.html"
    return FileResponse(index_path, media_type="text/html")

@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check"""
    if rag_chain is None:
        return {
            "status": "initializing",
            "message": "RAG system is still initializing"
        }
    return {
        "status": "healthy",
        "message": "All systems operational"
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a medical query using RAG
    
    Args:
        request: QueryRequest containing the medical question
    
    Returns:
        QueryResponse with answer and sources
    """
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        logger.info(f"Processing query: {request.query[:100]}...")
        result = rag_chain.generate_response(request.query)
        
        # Format response
        sources = [
            SourceMetadata(
                source=src.get("source"),
                page=src.get("page")
            )
            for src in result.get("sources", [])
        ]
        
        return QueryResponse(
            query=request.query,
            answer=result.get("answer", ""),
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/version")
async def get_version():
    """Get API version"""
    return {
        "version": "1.0.0",
        "name": "Medical Consultant API"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
