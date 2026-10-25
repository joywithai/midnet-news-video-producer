#!/usr/bin/env bash
set -e
command -v ffmpeg >/dev/null || { echo "Install FFmpeg first."; exit 1; }
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
printf '
Installed. Run: . .venv/bin/activate && python run_production.py
'
