---
name: midnet-news-video-producer
description: Produce a complete MidNet News YouTube package from audio, brief.md, and optional visuals. Use for audio-to-SRT, verified visual planning, branded news video rendering, thumbnails, metadata packaging, and media QC.
---

# MidNet News Video Producer

## Trigger
Use when the repository contains a new `input/brief.md` and narration audio and the user asks to create a complete news video package.

## Required workflow
1. Read `input/brief.md` and validate its English narration, resource names, three thumbnail ideas, three titles, and description.
2. Put user-owned or properly licensed visuals in `input/src/`. Never substitute unrelated event imagery.
3. Run `python3 run_production.py` from the repository root.
4. Inspect `production/productionReport.json`.
5. Do not claim completion unless `status` is `PASS` or `PASS_WITH_WARNINGS` and `newsVideo.mp4` fully decodes.
6. Return the production files, not internal reasoning.

## Safety and editorial rules
- Never fabricate an image, statistic, or attribution.
- Archive footage must include `archive` in its filename to receive an ARCHIVE label.
- User-provided media is treated as user-authorized; source information should be completed in `input/src/sources.json`.
- If visuals are missing, use branded text/data cards rather than unrelated stock footage.
- Do not change the supplied MidNet logo design.

## Command
```bash
python3 run_production.py --input input --output production
```
