---
module: overlay
tags: [module, overlay]
---

# Overlay

## Purpose

Renders the heads-up HUD on top of the poker client window using PyQt6. Displays equity, hand strength, and per-seat stats.

## Key Files

| File | Role |
|------|------|
| `src/overlay/hud.py` | Main HUD window, manages layout |
| `src/overlay/seat_hud.py` | Per-seat widget showing stats |
| `src/overlay/widget.py` | Base overlay widget (transparent, always-on-top) |
| `src/overlay/styles.py` | Qt stylesheets |

## Dependencies

→ `PyQt6` (UI framework)
→ [[Architecture/Modules/Engine|Engine]] (equity data to display)
→ [[Architecture/Modules/Tracking|Tracking]] (player stats to display)

## Open Issues

_None recorded._
