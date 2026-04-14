---
tags: [architecture]
---

# PokerLens — System Overview

## What It Does

Real-time poker overlay for private games. Captures the screen, recognises cards via a CNN, calculates hand equity, and displays a heads-up HUD for the hero seat.

## Data Flow

```
Screen capture (mss)
    └─→ Crop seat/board regions (Capture)
            └─→ CNN inference — 54 classes (Recognition)
                    └─→ Equity calculation (Engine)
                            └─→ PyQt6 HUD overlay (Overlay)
                                    └─→ Hand history & stats DB (Tracking)
```

## Module Map

| Module | Path | Role |
|--------|------|------|
| [[Architecture/Modules/Capture\|Capture]] | `src/capture/` | Screen grab, window detection, card cropping |
| [[Architecture/Modules/Recognition\|Recognition]] | `src/recognition/` | CNN model (54 classes), training, inference |
| [[Architecture/Modules/Engine\|Engine]] | `src/engine/` | Equity calc (preflop lookup + Monte Carlo) |
| [[Architecture/Modules/Overlay\|Overlay]] | `src/overlay/` | PyQt6 HUD widgets |
| [[Architecture/Modules/Tracking\|Tracking]] | `src/tracking/` | Hand history, player stats, SQLite DB |
| Common | `src/common/` | Shared constants |

## Entry Point

`railbird/main.py` wires all modules together.

## Key Design Decisions

- [[Decisions/001-CNN-vs-YOLO|001 — CNN vs YOLO]]
