# Frontend Connection Troubleshooting Guide

If your frontend isn't connecting to the FastAPI backend, follow these steps:

## Quick Checklist

- [ ] FastAPI backend is running (`python api.py`)
- [ ] Port 8000 is available
- [ ] Check browser console (F12) for errors
- [ ] API URL is correct in settings (⚙️ button)
- [ ] No firewall blocking connections

---

## Step-by-Step Troubleshooting

### 1. **Verify FastAPI is Running**

**Check if the API is actually running:**

```bash
# Terminal 1: Start the API
python api.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Test the API directly:**

```bash
# Terminal 2: Test API health
curl http://localhost:8000/health
```

Or visit in browser: `http://localhost:8000/health`

Expected response:
```json
{"status":"healthy","message":"All systems operational"}
```

---

### 2. **Check Port Availability**

Port 8000 might be in use. Check and free it:

**Windows PowerShell:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# If found, kill it (replace PID with the number from above)
taskkill /PID <PID> /F

# Or use a different port - edit api.py last line and change port=8000
```

**Linux/macOS:**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

---

### 3. **Verify API Endpoint**

**Check API Documentation:**

Visit: `http://localhost:8000/docs`

You should see Swagger UI with all endpoints.

**Test Query Endpoint Directly:**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is hypertension?"}'
```

---

### 4. **Check Browser Console**

Press `F12` → Console tab → Look for red errors

**Common Errors:**

**A) CORS Error**
```
Access to XMLHttpRequest at 'http://localhost:8000/query' 
has been blocked by CORS policy
```

**Solution:** CORS is already enabled in api.py. Make sure:
- You're not modifying the CORS middleware
- FastAPI is properly imported
- Restart the server

**B) Connection Refused**
```
Failed to fetch
TypeError: Failed to fetch
```

**Solution:**
- FastAPI is not running
- Port is wrong
- Firewall is blocking connections
- Try using `http://127.0.0.1:8000` instead of `http://localhost:8000`

**C) Network Request Failed**
```
Network error or timeout
```

**Solution:**
- Server is taking too long (increase timeout in index.html)
- Check if Ollama LLM is running
- Check if vector store is being initialized

---

### 5. **Configure API URL**

Click the **⚙️ Settings** button in top-right corner and update:

- Default: `http://localhost:8000`
- Remote: `http://your-ip:8000`
- Custom port: `http://localhost:8001` (if using different port)

---

### 6. **Check Ollama Connection**

The API depends on Ollama running for LLM:

```bash
# Make sure Ollama is running
ollama serve

# In another terminal, test Ollama
curl http://localhost:11434/api/health
```

If Ollama is not responding, you'll get "model not found" errors.

---

### 7. **Test Full Stack**

Complete test of entire system:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start FastAPI
python api.py

# Terminal 3: Run frontend
# Option A: Open index.html directly
# Option B: Serve with Python HTTP server
cd path/to/project
python -m http.server 8080

# Browser: http://localhost:8080
```

---

### 8. **Enable Debug Logging**

**In api.py**, add before app creation:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check terminal output for detailed error messages.

---

### 9. **Alternative Test Method**

**Create a simple test script (test_api.py):**

```python
import requests
import json

API_URL = "http://localhost:8000"

# Test 1: Health check
print("Testing /health...")
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    print(f"✓ Health: {response.json()}")
except Exception as e:
    print(f"✗ Health failed: {e}")

# Test 2: Query
print("\nTesting /query...")
try:
    response = requests.post(
        f"{API_URL}/query",
        json={"query": "What is hypertension?"},
        timeout=30
    )
    print(f"✓ Query response: {response.json()}")
except Exception as e:
    print(f"✗ Query failed: {e}")
```

Run with:
```bash
python test_api.py
```

---

### 10. **Network Configuration Issues**

**If using different machine for API:**

1. **Get your IP address:**
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Update API to listen on all interfaces:**
   
   In `api.py`, change the last line:
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(
           app,
           host="0.0.0.0",  # Listen on all interfaces
           port=8000
       )
   ```

3. **Update frontend URL** (⚙️ Settings):
   ```
   http://<your-ip>:8000
   ```

---

## Quick Fix Checklist

| Issue | Fix |
|-------|-----|
| "Failed to fetch" | Start FastAPI: `python api.py` |
| CORS error | Restart FastAPI, check middleware |
| "Cannot GET /health" | Wrong URL in settings |
| "Model not found" | Start Ollama: `ollama serve` |
| Timeout errors | Increase timeout in index.html or wait for embeddings |
| Port 8000 in use | Kill process or use different port |
| API returns 500 error | Check FastAPI terminal for error logs |

---

## Still Having Issues?

1. Check `logs/app.log` for errors
2. Check FastAPI terminal output for stack traces
3. Verify all dependencies: `pip install -r requirements.txt`
4. Restart everything from scratch
5. Try using Streamlit instead: `streamlit run streamlit_app.py`

---

## Contact & Support

For more help:
- Check [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
- Review [README.md](README.md)
- Check application logs in `logs/` directory
