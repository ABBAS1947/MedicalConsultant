# Medical Consultant AI - Complete Setup Guide

## Overview
This is a RAG (Retrieval-Augmented Generation) medical consultant AI that uses LangChain, Ollama, and ChromaDB to provide informed medical answers based on uploaded documents.

## Prerequisites

### System Requirements
- **Python 3.8+** (3.11 recommended)
- **Windows/Linux/macOS**
- **4GB+ RAM** (for embeddings)
- **Git** (for cloning if needed)

### Required Software
- **Ollama** - Local LLM server
- **Git** - Version control

---

## Step 1: Install Ollama

Ollama provides the local LLM that powers the AI responses.

### Windows
1. Download from: https://ollama.ai/download
2. Run the installer
3. Open Command Prompt and run:
   ```bash
   ollama serve
   ```

### Linux/macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

### Pull Required Model
```bash
ollama pull llama2:7b  # or any model you prefer
```

---

## Step 2: Clone/Download the Project

### Option A: Clone with Git
```bash
git clone <repository-url>
cd MedicalConsultant
```

### Option B: Download ZIP
- Download the project ZIP file
- Extract to a folder
- Open terminal in that folder

---

## Step 3: Set Up Python Environment

### Create Virtual Environment
```bash
# Windows
python -m venv .venv

# Linux/macOS
python3 -m venv .venv
```

### Activate Virtual Environment
```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat

# Linux/macOS
source .venv/bin/activate
```

**Note:** You should see `(.venv)` in your terminal prompt after activation.

---

## Step 4: Install Dependencies

### Install Python Packages
```bash
pip install -r requirements.txt
```

### Verify Installation
```bash
python -c "import langchain, chromadb, ollama; print('✓ All dependencies installed')"
```

---

## Step 5: Configure Environment

### Create Environment File (Optional)
Create `.env` file in the project root:
```env
# Model Configuration
MODEL_NAME=llama2:7b
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Database Configuration
CHROMA_DIR=vectorstore
DATA_PATH=data/raw

# Processing Configuration
CHUNK_SIZE=800
CHUNK_OVERLAP=150
TOP_K=3
```

### Add Medical Documents
1. Create folder: `data/raw/`
2. Add PDF files containing medical information
3. Supported formats: PDF

---

## Step 6: Initialize the System

### First-Time Setup
Run the ingestion pipeline to process documents and create embeddings:

```bash
python app.py
```

**What happens:**
- Loads PDF documents from `data/raw/`
- Cleans and processes text
- Splits into chunks
- Creates embeddings
- Stores in ChromaDB vector database

**Expected output:**
```
INFO: Starting ingestion pipeline...
INFO: Processing file: document1.pdf
INFO: Splitting completed. Total chunks: 150
INFO: Vector store created successfully.
```

---

## Step 7: Run the Application

### Option A: FastAPI Backend + HTML Frontend (Recommended)

#### Terminal 1: Start Ollama
```bash
ollama serve
```

#### Terminal 2: Start FastAPI Backend
```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1; python api.py

# Linux/macOS
source .venv/bin/activate && python api.py
```

**Expected output:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete.
```

#### Terminal 3: Start Web Server (Optional)
```bash
python -m http.server 8080
```

#### Open Browser
- **Direct:** Open `index.html` in browser
- **Via server:** Visit `http://localhost:8080`

### Option B: Streamlit Frontend (Alternative)

#### Terminal 1: Start Ollama
```bash
ollama serve
```

#### Terminal 2: Start Streamlit
```bash
streamlit run streamlit_app.py
```

**Opens automatically at:** `http://localhost:8501`

### Option C: CLI Only
```bash
python app.py
```

---

## Step 8: Test the System

### Health Check
Visit: `http://localhost:8000/health`

Expected response:
```json
{"status":"healthy","message":"All systems operational"}
```

### API Documentation
Visit: `http://localhost:8000/docs`

### Test Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of hypertension?"}'
```

---

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Ollama not responding
```bash
# Restart Ollama
ollama serve

# Check status
curl http://localhost:11434/api/health
```

### "Failed to fetch" in browser
- Ensure FastAPI is running on port 8000
- Check browser console for CORS errors
- Try refreshing the page

### Vector store errors
```bash
# Delete and recreate vector store
rmdir /s vectorstore
python app.py
```

### Memory issues
- Reduce `CHUNK_SIZE` in config
- Use smaller embedding model
- Add more RAM

---

## Configuration Options

### Model Selection
Edit `.env` or modify `config.py`:
```python
MODEL_NAME = "llama2:13b"  # Larger model for better answers
MODEL_NAME = "mistral:7b"  # Alternative model
```

### Processing Parameters
```python
CHUNK_SIZE = 500      # Smaller chunks = more precise answers
CHUNK_OVERLAP = 50    # Overlap between chunks
TOP_K = 5            # Number of sources to retrieve
```

### Embedding Models
```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"    # Fast, good quality
EMBEDDING_MODEL = "all-mpnet-base-v2"   # Slower, better quality
```

---

## File Structure

```
MedicalConsultant/
├── api.py                 # FastAPI backend server
├── app.py                 # CLI application
├── streamlit_app.py       # Streamlit web interface
├── index.html            # HTML frontend
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup
├── .env                  # Environment variables
├── data/
│   └── raw/              # PDF documents
├── vectorstore/          # ChromaDB database
├── src/
│   ├── __init__.py
│   └── components/
│       ├── loader.py     # PDF loading
│       ├── cleaner.py    # Text cleaning
│       ├── splitter.py   # Document splitting
│       ├── embedding.py  # Vector embeddings
│       ├── retriever.py  # Vector search
│       ├── rag_chain.py  # LLM integration
│       └── pipeline.py   # Main pipeline
│   └── utils/
│       ├── logger.py     # Logging
│       ├── prompt.py     # System prompts
│       └── exceptions.py # Custom exceptions
├── logs/                 # Application logs
└── research/             # Notebooks and experiments
```

---

## Advanced Usage

### Adding New Documents
1. Place PDFs in `data/raw/`
2. Run `python app.py` to reprocess
3. Or call the API endpoint: `POST /ingest`

### Custom Models
```bash
# Pull different models
ollama pull codellama:7b
ollama pull medical-llama:7b  # If available
```

### API Endpoints

#### GET `/health`
Check system status.

#### POST `/query`
Submit medical questions.
```json
{
  "query": "What are diabetes symptoms?"
}
```

#### GET `/docs`
Interactive API documentation.

---

## Performance Tips

- **Use SSD storage** for faster vector searches
- **Pre-load models** in Ollama for faster startup
- **Batch process** large document collections
- **Monitor RAM usage** during embedding creation
- **Use smaller chunks** for more precise answers

---

## Security Notes

- This is for **educational purposes only**
- **Not for clinical use** - always consult healthcare professionals
- Keep medical data **confidential** and **secure**
- Regular **backups** of vectorstore recommended

---

## Support

### Common Issues
- Check `logs/app.log` for detailed error messages
- Verify all services are running on correct ports
- Ensure virtual environment is activated

### Getting Help
- Check browser developer console (F12)
- Review terminal output for error messages
- Verify Ollama is responding: `ollama list`

---

## Quick Start Commands

```bash
# One-time setup
git clone <repo>
cd MedicalConsultant
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# Add documents to data/raw/
# Edit .env for configuration

# Daily usage
ollama serve                    # Terminal 1
.venv\Scripts\Activate.ps1; python api.py  # Terminal 2
# Open index.html in browser
```

---

**Ready to provide medical insights! 🏥**</content>
</xai:function_call">The comprehensive setup guide is now in your README.md! This covers everything from scratch installation to running the application, with troubleshooting and configuration options. The guide includes all three frontend options and detailed steps for each operating system.

