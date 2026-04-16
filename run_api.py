#!/usr/bin/env python
"""
Quick Startup Helper for Medical Consultant AI
Runs the FastAPI backend and provides connection instructions
"""

import subprocess
import time
import os
import sys
import webbrowser
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🏥 Medical Consultant AI - FastAPI Backend Server       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        print("✓ FastAPI and Uvicorn found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Install with: pip install -r requirements.txt")
        return False

def start_server():
    """Start the FastAPI server"""
    print_banner()
    
    if not check_dependencies():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🚀 Starting FastAPI Server...")
    print("="*60)
    
    try:
        # Run the API server
        subprocess.run(
            [sys.executable, "api.py"],
            cwd=str(Path(__file__).parent)
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
