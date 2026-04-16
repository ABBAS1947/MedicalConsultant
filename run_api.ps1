# Medical Consultant AI - FastAPI Server Launcher
# PowerShell Script for Windows

Write-Host "`n============================================================"
Write-Host "  🏥 Medical Consultant AI - FastAPI Backend Server"
Write-Host "============================================================`n"

# Activate virtual environment
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated`n"
} else {
    Write-Host "❌ Virtual environment not found"
    Write-Host "Run: python -m venv .venv`n"
    exit 1
}

# Check dependencies
try {
    python -c "import fastapi, uvicorn" 2>$null
    Write-Host "✓ FastAPI dependencies found`n"
} catch {
    Write-Host "📦 Installing dependencies..."
    pip install -r requirements.txt
}

Write-Host "============================================================"
Write-Host "🚀 Starting FastAPI Server...`n"
Write-Host "✓ Backend API: http://localhost:8000"
Write-Host "✓ API Docs: http://localhost:8000/docs"
Write-Host "✓ Health Check: http://localhost:8000/health`n"
Write-Host "📝 Frontend Options:"
Write-Host "   1. Open index.html directly in your browser"
Write-Host "   2. Run: python -m http.server 8080 (in another terminal)`n"
Write-Host "⏹️  To stop: Press Ctrl+C`n"
Write-Host "============================================================`n"

# Start the server
python api.py

Write-Host "✓ Server stopped"
