# Quick Start Guide - Frontend Setup

## Prerequisites

✓ Virtual environment activated
✓ Dependencies installed: `pip install -r requirements.txt`
✓ Ollama running (for LLM): `ollama serve`

---

## Option A: Use FastAPI + HTML Frontend (Recommended)

### Step 1: Start the Backend API

**Windows PowerShell:**
```powershell
.\run_api.ps1
```

**Windows Command Prompt:**
```cmd
run_api.bat
```

**Any OS:**
```bash
python api.py
```

✓ You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`

### Step 2: Open the Frontend

**Option 1 - Direct (Simplest):**
- Simply open `index.html` in your web browser
- Status will show ⏳ until API initializes, then ✓

**Option 2 - HTTP Server:**
```bash
# In a new terminal
python -m http.server 8080
```
- Then visit: `http://localhost:8080`

### Step 3: Test the Connection

1. Watch the status indicator in top-right (should show ✓ green)
2. If it shows ✗ red, click ⚙️ settings to configure API URL
3. Try asking a question

---

## Option B: Use Streamlit (Alternative)

```bash
streamlit run streamlit_app.py
```

Opens automatically at: `http://localhost:8501`

---

## How It Works

```
Your Browser (index.html)
        ↓
    HTML/CSS/JS Frontend
        ↓
    Sends query via HTTP POST
        ↓
    FastAPI Backend (api.py)
        ↓
    RAG System (src/components/)
        ↓
    Ollama LLM + Vector Store
        ↓
    Sends answer back to frontend
        ↓
    Displays in browser
```

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Status shows ✗ | API not running. Run `python api.py` |
| "Failed to fetch" | Make sure FastAPI is running on port 8000 |
| CORS Error in console | Restart FastAPI server |
| Timeout errors | Wait a bit - embeddings are being loaded |
| Port 8000 already in use | Stop other process or edit api.py to use different port |
| Ollama errors | Start Ollama: `ollama serve` |

**More help:** See `CONNECTION_TROUBLESHOOTING.md`

---

## API Endpoints You Can Test

**In browser:**
- Health: `http://localhost:8000/health`
- Docs: `http://localhost:8000/docs`

**With curl:**
```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?"}'
```

---

## Multiple Terminals Setup (Recommended)

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - FastAPI:**
```bash
python api.py
```

**Terminal 3 - HTTP Server (optional):**
```bash
python -m http.server 8080
```

**Browser:**
- `http://localhost:8080/index.html` (if using HTTP server)
- Or just open `index.html` directly

---

## Settings (⚙️ Button)

Click the ⚙️ gear icon in top-right to:
- Change API URL if running on different machine
- Typically: `http://localhost:8000` (default)
- For remote: `http://your-ip:8000`

---

## Tips

- First query might take 30+ seconds (embeddings)
- Click ⚙️ to see/change API URL if connection fails
- Status indicator auto-updates every 10 seconds
- Browser console (F12) shows detailed connection info
- Check `logs/app.log` for backend errors

---

Enjoy your Medical Consultant AI frontend! 🏥
