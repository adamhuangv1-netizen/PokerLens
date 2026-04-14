---
module: capture
tags: [module, capture]
---

# Capture

## Purpose

Detects the poker client window, captures the screen with `mss`, and crops individual card regions for each seat and the community board. Feeds raw image crops to [[Architecture/Modules/Recognition|Recognition]].

## Key Files

| File | Role |
|------|------|
| `src/capture/window.py` | Window detection via `pygetwindow` |
| `src/capture/screenshot.py` | Screen capture with `mss` |
| `src/capture/cropper.py` | Crops seat and board regions from screenshot |
| `src/capture/calibrator.py` | Interactive calibration of crop coordinates |
| `src/capture/collector.py` | Collects training images from live captures |
| `src/capture/pipeline.py` | Orchestrates the full capture → crop pipeline |
| `src/capture/log_tailer.py` | Tails poker client log files for hand events |

## Dependencies

→ [[Architecture/Modules/Recognition|Recognition]] (receives crops)
→ `src/common/constants.py` (shared labels/config)

## Open Issues

_None recorded._
