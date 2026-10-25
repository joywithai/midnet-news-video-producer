@echo off
where ffmpeg >nul 2>nul || (echo Install FFmpeg first. & exit /b 1)
python -m venv .venv
call .venv\Scriptsctivate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Installed. Run: python run_production.py
