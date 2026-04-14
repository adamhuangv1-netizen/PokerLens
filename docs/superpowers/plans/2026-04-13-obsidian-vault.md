# Obsidian Vault Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a fully configured Obsidian vault at `docs/obsidian/` inside the repo, serving as dev notebook, project wiki, and AI handoff hub.

**Architecture:** Hybrid folder structure (type-based top level: Architecture, Decisions, Sessions, Roadmap, Reference) with module tags for cross-cutting filtering. Obsidian config committed to git (minus workspace state files). Seed content pre-populated from current codebase.

**Tech Stack:** Obsidian markdown, JSON config files, Dataview community plugin (installed by user via Obsidian), git

---

## File Map

### Created by this plan

```
docs/obsidian/
├── Home.md
├── Architecture/
│   ├── Overview.md
│   └── Modules/
│       ├── Capture.md
│       ├── Recognition.md
│       ├── Engine.md
│       ├── Overlay.md
│       └── Tracking.md
├── Decisions/
│   └── 001-CNN-vs-YOLO.md
├── Sessions/             (empty dir — placeholder .gitkeep)
├── Roadmap/
│   ├── Backlog.md
│   └── Milestones.md
└── Reference/
    ├── Dependencies.md
    └── Glossary.md

docs/obsidian/.obsidian/
├── app.json
├── appearance.json
├── core-plugins.json
├── community-plugins.json
├── templates.json
└── templates/
    ├── ADR.md
    └── Session Log.md
```

### Modified by this plan

- `.gitignore` — add Obsidian workspace state and plugin binary exclusions

---

## Task 1: Directory scaffold and .gitignore

**Files:**
- Create: `docs/obsidian/Sessions/.gitkeep`
- Modify: `.gitignore`

- [ ] **Step 1: Create the vault directory tree**

```bash
mkdir -p docs/obsidian/Architecture/Modules
mkdir -p docs/obsidian/Decisions
mkdir -p docs/obsidian/Sessions
mkdir -p docs/obsidian/Roadmap
mkdir -p docs/obsidian/Reference
mkdir -p docs/obsidian/.obsidian/templates
touch docs/obsidian/Sessions/.gitkeep
```

- [ ] **Step 2: Verify directories exist**

```bash
find docs/obsidian -type d | sort
```

Expected output:
```
docs/obsidian
docs/obsidian/.obsidian
docs/obsidian/.obsidian/templates
docs/obsidian/Architecture
docs/obsidian/Architecture/Modules
docs/obsidian/Decisions
docs/obsidian/Reference
docs/obsidian/Roadmap
docs/obsidian/Sessions
```

- [ ] **Step 3: Add gitignore entries**

Append to `.gitignore`:

```
# Obsidian vault — workspace state (changes on every launch, do not commit)
docs/obsidian/.obsidian/workspace.json
docs/obsidian/.obsidian/workspace-mobile.json
# Obsidian plugin binaries (install via Obsidian community plugin browser)
docs/obsidian/.obsidian/plugins/
```

- [ ] **Step 4: Commit**

```bash
git add docs/obsidian/Sessions/.gitkeep .gitignore
git commit -m "chore: scaffold obsidian vault directories and gitignore"
```

---

## Task 2: Obsidian configuration files

**Files:**
- Create: `docs/obsidian/.obsidian/app.json`
- Create: `docs/obsidian/.obsidian/appearance.json`
- Create: `docs/obsidian/.obsidian/core-plugins.json`
- Create: `docs/obsidian/.obsidian/community-plugins.json`
- Create: `docs/obsidian/.obsidian/templates.json`

- [ ] **Step 1: Create app.json**

`docs/obsidian/.obsidian/app.json`:
```json
{
  "legacyEditor": false,
  "livePreview": true,
  "defaultViewMode": "source"
}
```

- [ ] **Step 2: Create appearance.json**

`docs/obsidian/.obsidian/appearance.json`:
```json
{
  "theme": "moonstone"
}
```

- [ ] **Step 3: Create core-plugins.json**

`docs/obsidian/.obsidian/core-plugins.json`:
```json
[
  "file-explorer",
  "global-search",
  "switcher",
  "graph",
  "backlink",
  "outgoing-link",
  "tag-pane",
  "templates",
  "command-palette",
  "word-count"
]
```

- [ ] **Step 4: Create community-plugins.json**

`docs/obsidian/.obsidian/community-plugins.json`:
```json
["dataview"]
```

- [ ] **Step 5: Create templates.json** (tells Templates core plugin where templates live)

`docs/obsidian/.obsidian/templates.json`:
```json
{
  "folder": ".obsidian/templates",
  "dateFormat": "YYYY-MM-DD",
  "timeFormat": "HH:mm"
}
```

- [ ] **Step 6: Validate all JSON files are parseable**

```bash
python -c "
import json, pathlib
for f in pathlib.Path('docs/obsidian/.obsidian').glob('*.json'):
    json.loads(f.read_text())
    print(f'OK: {f.name}')
"
```

Expected output:
```
OK: app.json
OK: appearance.json
OK: community-plugins.json
OK: core-plugins.json
OK: templates.json
```

- [ ] **Step 7: Commit**

```bash
git add docs/obsidian/.obsidian/
git commit -m "chore: add obsidian config (core plugins, dataview, templates)"
```

---

## Task 3: Note templates

**Files:**
- Create: `docs/obsidian/.obsidian/templates/ADR.md`
- Create: `docs/obsidian/.obsidian/templates/Session Log.md`

- [ ] **Step 1: Create ADR template**

`docs/obsidian/.obsidian/templates/ADR.md`:
```markdown
---
title: 
date: {{date}}
status: open
modules: []   # pick from: capture, recognition, engine, overlay, tracking
---

## Context

## Decision

## Consequences
```

- [ ] **Step 2: Create Session Log template**

`docs/obsidian/.obsidian/templates/Session Log.md`:
```markdown
---
date: {{date}}
tags: [session]
modules: []   # pick from: capture, recognition, engine, overlay, tracking
---

## Focus

## What was done

## Decisions made
<!-- link to ADRs: [[Decisions/NNN-title]] -->

## Open questions

## Next steps
```

- [ ] **Step 3: Verify both template files exist**

```bash
ls docs/obsidian/.obsidian/templates/
```

Expected output:
```
ADR.md  Session Log.md
```

- [ ] **Step 4: Commit**

```bash
git add docs/obsidian/.obsidian/templates/
git commit -m "chore: add ADR and Session Log note templates"
```

---

## Task 4: Architecture seed notes

**Files:**
- Create: `docs/obsidian/Architecture/Overview.md`
- Create: `docs/obsidian/Architecture/Modules/Capture.md`
- Create: `docs/obsidian/Architecture/Modules/Recognition.md`
- Create: `docs/obsidian/Architecture/Modules/Engine.md`
- Create: `docs/obsidian/Architecture/Modules/Overlay.md`
- Create: `docs/obsidian/Architecture/Modules/Tracking.md`

- [ ] **Step 1: Create Overview.md**

`docs/obsidian/Architecture/Overview.md`:
```markdown
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
```

- [ ] **Step 2: Create Capture.md**

`docs/obsidian/Architecture/Modules/Capture.md`:
```markdown
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
```

- [ ] **Step 3: Create Recognition.md**

`docs/obsidian/Architecture/Modules/Recognition.md`:
```markdown
---
module: recognition
tags: [module, recognition]
---

# Recognition

## Purpose

Runs CNN inference on card image crops. Classifies each crop into one of 54 classes: 52 playing cards + `empty` (no card) + `back` (face-down card). Feeds predictions to [[Architecture/Modules/Engine|Engine]].

## Key Files

| File | Role |
|------|------|
| `src/recognition/model.py` | CNN architecture definition |
| `src/recognition/dataset.py` | PyTorch dataset for training images |
| `src/recognition/inference.py` | Loads ONNX model, runs inference on crops |
| `railbird/train.py` | Training script |
| `railbird/scripts/augment.py` | Data augmentation pipeline |
| `railbird/scripts/generate_synthetic_cards.py` | Synthetic training data generation |

## Class Structure

54 output classes:
- 52 standard playing cards (rank + suit, e.g. `Ah`, `Kd`, `2c`)
- `empty` — no card in the region
- `back` — face-down card visible

## Dependencies

→ `torch`, `torchvision` (training)
→ `onnxruntime` (inference)
→ `Pillow`, `opencv-python` (image processing)
→ [[Architecture/Modules/Capture|Capture]] (receives crops)

## Open Issues

_None recorded._
```

- [ ] **Step 4: Create Engine.md**

`docs/obsidian/Architecture/Modules/Engine.md`:
```markdown
---
module: engine
tags: [module, engine]
---

# Engine

## Purpose

Calculates hero hand equity given recognised cards. Uses a pre-computed lookup table for pre-flop speed, and Monte Carlo simulation (eval7) for post-flop streets.

## Key Files

| File | Role |
|------|------|
| `src/engine/equity.py` | `EquityCalculator` — main public interface |
| `src/engine/lookup.py` | `PreflopTable` — loads and queries `preflop_equity.json` |
| `src/engine/strategy.py` | Strategy recommendations based on equity |
| `railbird/data/preflop_equity.json` | Pre-computed lookup table (committed to git) |
| `railbird/scripts/generate_preflop_table.py` | Script to regenerate the lookup table |

## Equity Strategy

- **Pre-flop:** `PreflopTable` lookup (~0 ms, uses `preflop_equity.json`)
- **Post-flop:** Monte Carlo with `eval7` (~20–40 ms for 5,000 simulations)
- **Fallback:** `treys` library if `eval7` is not installed

## Output

`EquityResult(equity, hand_strength, street, hand_class, simulations)`

`hand_strength` ∈ {`strong`, `medium`, `marginal`, `weak`}

## Dependencies

→ `eval7` (primary evaluator, C-backed)
→ `treys` (fallback evaluator)
→ [[Architecture/Modules/Recognition|Recognition]] (card labels)

## Open Issues

_None recorded._
```

- [ ] **Step 5: Create Overlay.md**

`docs/obsidian/Architecture/Modules/Overlay.md`:
```markdown
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
```

- [ ] **Step 6: Create Tracking.md**

`docs/obsidian/Architecture/Modules/Tracking.md`:
```markdown
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
```

- [ ] **Step 7: Verify all 6 architecture notes exist**

```bash
find docs/obsidian/Architecture -name "*.md" | sort
```

Expected output:
```
docs/obsidian/Architecture/Modules/Capture.md
docs/obsidian/Architecture/Modules/Engine.md
docs/obsidian/Architecture/Modules/Overlay.md
docs/obsidian/Architecture/Modules/Recognition.md
docs/obsidian/Architecture/Modules/Tracking.md
docs/obsidian/Architecture/Overview.md
```

- [ ] **Step 8: Commit**

```bash
git add docs/obsidian/Architecture/
git commit -m "docs: add architecture overview and module seed notes to obsidian vault"
```

---

## Task 5: Decisions, Roadmap, and Reference seed notes

**Files:**
- Create: `docs/obsidian/Decisions/001-CNN-vs-YOLO.md`
- Create: `docs/obsidian/Roadmap/Backlog.md`
- Create: `docs/obsidian/Roadmap/Milestones.md`
- Create: `docs/obsidian/Reference/Dependencies.md`
- Create: `docs/obsidian/Reference/Glossary.md`

- [ ] **Step 1: Create ADR 001**

`docs/obsidian/Decisions/001-CNN-vs-YOLO.md`:
```markdown
---
title: CNN vs YOLO for Card Recognition
date: 2026-04-13
status: decided
modules: [recognition]
---

# 001 — CNN vs YOLO for Card Recognition

## Context

Needed to choose an architecture for recognising playing cards in cropped screen regions. Initial options were a spatial CNN classifier or YOLO-style object detection.

## Decision

**Spatial CNN with 54 output classes.**

54 classes = 52 standard playing cards + `empty` (no card present) + `back` (face-down card).

## Consequences

- Simpler training pipeline — standard image classification, no bounding box labels needed
- Fast inference on fixed-size crops (cropper handles localisation, model handles classification)
- 54-class model scaffolded in `src/recognition/model.py` and `train.py`
- YOLO not needed: card positions are determined by calibrated crop regions, not detection
```

- [ ] **Step 2: Create Backlog.md**

`docs/obsidian/Roadmap/Backlog.md`:
```markdown
---
tags: [roadmap]
---

# Backlog

## In Progress

_Nothing active — add items here during sessions._

## Pending

- [ ] Complete CNN training pipeline end-to-end
- [ ] Calibrate crop regions for target poker client
- [ ] Build first working HUD prototype
- [ ] Wire equity results into HUD display
- [ ] Add VPIP/PFR stats to Tracking module
- [ ] Test hand tracker state machine

## Done

- [x] Chose CNN architecture (54 classes) over YOLO — see [[Decisions/001-CNN-vs-YOLO]]
- [x] Scaffolded all 6 modules (`capture`, `recognition`, `engine`, `overlay`, `tracking`, `common`)
- [x] Implemented `EquityCalculator` with eval7 + treys fallback
- [x] Generated pre-flop equity lookup table (`preflop_equity.json`)
```

- [ ] **Step 3: Create Milestones.md**

`docs/obsidian/Roadmap/Milestones.md`:
```markdown
---
tags: [roadmap]
---

# Milestones

## M1 — Working Card Recognition

- Trained CNN reaching >95% validation accuracy on real captures
- Inference pipeline running in real time

## M2 — First Working HUD

- Overlay displays hero equity on screen during a live game
- Pre-flop lookup + post-flop Monte Carlo both functional

## M3 — Stats Tracking

- Hand history persisted to SQLite
- VPIP/PFR shown per opponent seat in HUD

## M4 — Polish

- Calibration UI complete
- Performance profiled and within real-time budget
```

- [ ] **Step 4: Create Dependencies.md**

`docs/obsidian/Reference/Dependencies.md`:
```markdown
---
tags: [reference]
---

# Dependencies

From `railbird/requirements.txt`:

| Package | Min Version | Used By |
|---------|-------------|---------|
| `mss` | 9.0.0 | [[Architecture/Modules/Capture\|Capture]] — fast cross-platform screen capture |
| `opencv-python` | 4.8.0 | Capture, Recognition — image processing |
| `numpy` | 1.24.0 | Recognition, Engine — array operations |
| `Pillow` | 10.0.0 | Recognition — image loading/transforms |
| `torch` | 2.0.0 | [[Architecture/Modules/Recognition\|Recognition]] — CNN training |
| `torchvision` | 0.15.0 | Recognition — transforms, pretrained models |
| `onnxruntime` | 1.16.0 | Recognition — fast ONNX inference |
| `eval7` | 0.1.9 | [[Architecture/Modules/Engine\|Engine]] — C-backed hand evaluator (primary) |
| `PyQt6` | 6.5.0 | [[Architecture/Modules/Overlay\|Overlay]] — HUD framework |
| `pynput` | 1.7.0 | Global keyboard/mouse hooks |
| `pygetwindow` | 0.0.9 | Capture — window detection |

Install: `pip install -r railbird/requirements.txt`

### Optional

- `treys` — fallback hand evaluator if `eval7` unavailable (`pip install treys`)
```

- [ ] **Step 5: Create Glossary.md**

`docs/obsidian/Reference/Glossary.md`:
```markdown
---
tags: [reference]
---

# Glossary

**ADR** — Architecture Decision Record. A note documenting a significant design choice, its context, and consequences. Stored in `Decisions/`.

**back** — CNN class label for a face-down card (card back visible, rank/suit unknown).

**empty** — CNN class label for a seat or board position with no card present.

**equity** — Hero's probability of winning the hand. Expressed as a float in [0, 1]. Computed by [[Architecture/Modules/Engine|Engine]].

**eval7** — C-backed Python poker hand evaluator. Primary backend for Monte Carlo simulations.

**HUD** — Heads-Up Display. The PyQt6 overlay rendered on top of the poker client window.

**Monte Carlo** — Simulation-based equity calculation. Randomly deals remaining cards and counts win/tie/loss outcomes over N trials. Used post-flop (~5,000 simulations).

**PFR** — Pre-Flop Raise percentage. Stat tracked per player in [[Architecture/Modules/Tracking|Tracking]].

**preflop_equity.json** — Pre-computed lookup table mapping hand classes (e.g. `AKs`) to equity values for 1–9 opponents. Lives at `railbird/data/preflop_equity.json`.

**railbird** — Internal codename for the project (a railbird is someone who watches a poker game without playing).

**seat** — A numbered position at the poker table. The overlay tracks 2–9 seats.

**VPIP** — Voluntarily Put money In Pot percentage. Key stat for classifying player aggression. Tracked by [[Architecture/Modules/Tracking|Tracking]].
```

- [ ] **Step 6: Verify all files exist**

```bash
find docs/obsidian/Decisions docs/obsidian/Roadmap docs/obsidian/Reference -name "*.md" | sort
```

Expected output:
```
docs/obsidian/Decisions/001-CNN-vs-YOLO.md
docs/obsidian/Reference/Dependencies.md
docs/obsidian/Reference/Glossary.md
docs/obsidian/Roadmap/Backlog.md
docs/obsidian/Roadmap/Milestones.md
```

- [ ] **Step 7: Commit**

```bash
git add docs/obsidian/Decisions/ docs/obsidian/Roadmap/ docs/obsidian/Reference/
git commit -m "docs: add ADR 001, roadmap, and reference notes to obsidian vault"
```

---

## Task 6: Home dashboard

**Files:**
- Create: `docs/obsidian/Home.md`

- [ ] **Step 1: Create Home.md**

`docs/obsidian/Home.md`:
```markdown
---
tags: [home]
---

# PokerLens Knowledge Base

> **Setup:** Install [Dataview](https://github.com/blacksmithgu/obsidian-dataview) via Obsidian's community plugin browser (Settings → Community plugins → Browse → search "Dataview") to enable the live queries below.

---

## Open Decisions

```dataview
table date, modules from "Decisions"
where status = "open"
sort date desc
```

## Recent Sessions

```dataview
table date, modules from "Sessions"
sort date desc
limit 7
```

---

## Modules

[[Architecture/Modules/Capture|Capture]] · [[Architecture/Modules/Recognition|Recognition]] · [[Architecture/Modules/Engine|Engine]] · [[Architecture/Modules/Overlay|Overlay]] · [[Architecture/Modules/Tracking|Tracking]]

---

## Quick Links

- [[Architecture/Overview|System Overview]]
- [[Roadmap/Backlog|Backlog]]
- [[Roadmap/Milestones|Milestones]]
- [[Reference/Dependencies|Dependencies]]
- [[Reference/Glossary|Glossary]]
```

- [ ] **Step 2: Verify Home.md exists**

```bash
ls docs/obsidian/Home.md
```

Expected output:
```
docs/obsidian/Home.md
```

- [ ] **Step 3: Verify full vault structure**

```bash
find docs/obsidian -not -path '*/.git/*' | sort
```

Expected output (all vault files present):
```
docs/obsidian
docs/obsidian/.obsidian
docs/obsidian/.obsidian/app.json
docs/obsidian/.obsidian/appearance.json
docs/obsidian/.obsidian/community-plugins.json
docs/obsidian/.obsidian/core-plugins.json
docs/obsidian/.obsidian/templates
docs/obsidian/.obsidian/templates/ADR.md
docs/obsidian/.obsidian/templates/Session Log.md
docs/obsidian/.obsidian/templates.json
docs/obsidian/Architecture
docs/obsidian/Architecture/Modules
docs/obsidian/Architecture/Modules/Capture.md
docs/obsidian/Architecture/Modules/Engine.md
docs/obsidian/Architecture/Modules/Overlay.md
docs/obsidian/Architecture/Modules/Recognition.md
docs/obsidian/Architecture/Modules/Tracking.md
docs/obsidian/Architecture/Overview.md
docs/obsidian/Decisions
docs/obsidian/Decisions/001-CNN-vs-YOLO.md
docs/obsidian/Home.md
docs/obsidian/Reference
docs/obsidian/Reference/Dependencies.md
docs/obsidian/Reference/Glossary.md
docs/obsidian/Roadmap
docs/obsidian/Roadmap/Backlog.md
docs/obsidian/Roadmap/Milestones.md
docs/obsidian/Sessions
docs/obsidian/Sessions/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add docs/obsidian/Home.md
git commit -m "docs: add obsidian vault home dashboard with dataview queries"
```

---

## Post-implementation: Open the vault in Obsidian

1. Open Obsidian → **Open folder as vault** → select `docs/obsidian/`
2. Go to **Settings → Community plugins → Browse** → search "Dataview" → Install → Enable
3. Navigate to `Home.md` — the Dataview queries will now render live
4. Confirm the Open Decisions table shows `001-CNN-vs-YOLO` with `status: decided` (it should NOT appear — status is `decided`, not `open`)
5. Confirm the Recent Sessions table is empty (no sessions yet — correct)
6. Click any `[[wikilink]]` — confirm it resolves to the correct note
