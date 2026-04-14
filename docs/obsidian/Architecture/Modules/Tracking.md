---
module: tracking
tags: [module, tracking]
---

# Tracking

## Purpose

Records hand history and computes player statistics (VPIP, PFR, etc.) to a local SQLite database. Stats are surfaced in the [[Architecture/Modules/Overlay|Overlay]].

## Key Files

| File | Role |
|------|------|
| `src/tracking/database.py` | SQLite schema and CRUD operations |
| `src/tracking/hand_tracker.py` | Tracks current hand state machine |
| `src/tracking/stats.py` | Computes player statistics from hand history |
| `railbird/tests/test_stats.py` | Unit tests for stats calculations |

## Dependencies

→ SQLite (Python stdlib `sqlite3`)
→ [[Architecture/Modules/Recognition|Recognition]] (card events)
→ [[Architecture/Modules/Capture|Capture]] (hand events from log tailer)

## Open Issues

_None recorded._
