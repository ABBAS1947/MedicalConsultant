@echo off
REM Medical Consultant AI - FastAPI Server Launcher
REM Windows Batch Script

cls
echo.
echo ============================================================
echo   Medical Consultant AI - FastAPI Backend Server
echo ============================================================
echo.

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo WARNING: Virtual environment not found
    echo Run: python -m venv .venv
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo ============================================================
echo Starting FastAPI Server...
echo.
echo Server will run at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo For Frontend:
echo - Option 1: Open index.html in browser
echo - Option 2: http://localhost:8080 (if using http.server)
echo.
echo To stop the server, press Ctrl+C
echo ============================================================
echo.

python api.py

pause
