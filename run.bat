@echo off
REM One-click launcher for the Multilingual Lyric Generator (PS-C2).
REM Creates the venv + installs deps on first run, then starts the app.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment...
    python -m venv .venv
    echo [setup] Installing dependencies...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

if not exist ".env" (
    echo [note] No .env found. Copying .env.example -> .env
    echo        Edit .env and add your free GEMINI_API_KEY for real lyrics.
    copy /Y ".env.example" ".env" >nul
)

echo [run] Starting Streamlit on http://localhost:8501 ...
.venv\Scripts\python.exe -m streamlit run app.py
