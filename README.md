# MidNet News Video Producer

Git-ready, AI-agent-friendly production system for turning `audio + brief.md + optional visuals` into a branded 16:9 news video, subtitles, three thumbnail candidates, upload metadata, source record, and QC report.

## Quick start

```bash
bash scripts/install.sh
cp your-audio.wav input/audio.wav
cp your-brief.md input/brief.md
# Optional: add images/video to input/src/
python3 run_production.py
```

Windows:

```powershell
scripts\install.bat
python run_production.py
```

Final files are written to `production/`.

## Input contract

- `input/audio.wav`, `input/audio.mp3`, `input/audio.m4a`, or `input/audio.aac`
- `input/brief.md`
- optional assets in `input/src/`

The brief parser understands the MidNet v7 headings: Full News, English, বাংলা অর্থ, Photo / Resource Names, Thumbnail Ideas, Titles, and Description.

## Execution modes

- **Full mode:** FFmpeg + faster-whisper installed. Script-aligned subtitles, visuals, render, thumbnails, and QC.
- **Portable mode:** FFmpeg installed, but Whisper unavailable. The English script is evenly timestamped across the audio.
- **Asset-light mode:** If no source visuals exist, the renderer creates professional branded news cards instead of inventing or misrepresenting imagery.

## Design principles

- Original MidNet logo is preserved and used as a transparent corner watermark.
- 1920x1080, 30 fps, H.264 video, AAC 48 kHz audio.
- Navy, white, red U.S. broadcast-news visual language.
- Conservative visuals: local verified media first; no automatic unlicensed scraping.
- Captions remain within safe zones and avoid the logo.
- Every production receives technical and editorial consistency checks.

See `docs/USAGE.md`, `docs/BRIEF_FORMAT.md`, and `SKILL.md`.
