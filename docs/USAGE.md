# Usage

1. Replace `input/brief.md` with a final MidNet v7 brief.
2. Add one narration file named `audio.wav` or `audio.mp3`.
3. Add owned/licensed media to `input/src/` and document it in `sources.json`.
4. Run `python3 run_production.py`.
5. Open `production/productionReport.json`; verify PASS.

The system deliberately renders branded cards when no verified imagery is available. This avoids attaching unrelated photographs to a news event.
