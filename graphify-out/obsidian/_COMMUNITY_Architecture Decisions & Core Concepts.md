---
type: community
cohesion: 0.10
members: 41
---

# Architecture Decisions & Core Concepts

**Cohesion:** 0.10 - loosely connected
**Members:** 41 nodes

## Members
- [[54-Class CNN Card Classifier]] - document - docs/obsidian/Decisions/001-CNN-vs-YOLO.md
- [[ADR 001 CNN vs YOLO for Card Recognition]] - document - docs/obsidian/Decisions/001-CNN-vs-YOLO.md
- [[Architecture Decision Record (ADR)]] - document - docs/obsidian/Reference/Glossary.md
- [[Capture Module]] - document - docs/obsidian/Architecture/Modules/Capture.md
- [[Dependencies Reference]] - document - docs/obsidian/Reference/Dependencies.md
- [[Engine Module]] - document - docs/obsidian/Architecture/Modules/Engine.md
- [[EquityCalculator_1]] - document - docs/obsidian/Architecture/Modules/Engine.md
- [[EquityResult Output Type]] - document - docs/obsidian/Architecture/Modules/Engine.md
- [[Glossary Reference]] - document - docs/obsidian/Reference/Glossary.md
- [[Hand Tracker State Machine]] - document - docs/obsidian/Architecture/Modules/Tracking.md
- [[Heads-Up Display (HUD)]] - document - docs/obsidian/Architecture/Modules/Overlay.md
- [[M1 Working Card Recognition]] - document - docs/obsidian/Roadmap/Milestones.md
- [[M2 First Working HUD]] - document - docs/obsidian/Roadmap/Milestones.md
- [[M3 Stats Tracking]] - document - docs/obsidian/Roadmap/Milestones.md
- [[M4 Polish]] - document - docs/obsidian/Roadmap/Milestones.md
- [[Monte Carlo Equity Simulation]] - document - docs/obsidian/Architecture/Modules/Engine.md
- [[Obsidian Vault Design Spec]] - document - docs/superpowers/specs/2026-04-13-obsidian-vault-design.md
- [[Obsidian Vault Implementation Plan]] - document - docs/superpowers/plans/2026-04-13-obsidian-vault.md
- [[Overlay Module]] - document - docs/obsidian/Architecture/Modules/Overlay.md
- [[Pillow]] - document - docs/obsidian/Reference/Dependencies.md
- [[PokerLens Knowledge Base Home Dashboard]] - document - docs/obsidian/Home.md
- [[PokerLens System Overview]] - document - docs/obsidian/Architecture/Overview.md
- [[PreflopTable Lookup (preflop_equity.json)]] - document - docs/obsidian/Architecture/Modules/Engine.md
- [[Project Backlog]] - document - docs/obsidian/Roadmap/Backlog.md
- [[Project Milestones]] - document - docs/obsidian/Roadmap/Milestones.md
- [[PyQt6]] - document - docs/obsidian/Reference/Dependencies.md
- [[Rationale CNN chosen over YOLO (simpler pipeline, no bbox labels)]] - document - docs/obsidian/Decisions/001-CNN-vs-YOLO.md
- [[Rationale Type-based top-level folders with module tags for cross-cutting]] - document - docs/superpowers/specs/2026-04-13-obsidian-vault-design.md
- [[Rationale Vault committed to git for AI agent access and history]] - document - docs/superpowers/specs/2026-04-13-obsidian-vault-design.md
- [[Recognition Module]] - document - docs/obsidian/Architecture/Modules/Recognition.md
- [[SQLite Hand History Database]] - document - docs/obsidian/Architecture/Modules/Tracking.md
- [[Tracking Module]] - document - docs/obsidian/Architecture/Modules/Tracking.md
- [[VPIP  PFR Player Stats]] - document - docs/obsidian/Architecture/Modules/Tracking.md
- [[YOLO Object Detection (rejected alternative)]] - document - docs/obsidian/Decisions/001-CNN-vs-YOLO.md
- [[eval7 (C-backed hand evaluator)]] - document - docs/obsidian/Reference/Dependencies.md
- [[mss (screen capture library)]] - document - docs/obsidian/Reference/Dependencies.md
- [[onnxruntime]] - document - docs/obsidian/Reference/Dependencies.md
- [[opencv-python]] - document - docs/obsidian/Reference/Dependencies.md
- [[pygetwindow]] - document - docs/obsidian/Reference/Dependencies.md
- [[torch  torchvision]] - document - docs/obsidian/Reference/Dependencies.md
- [[treys (fallback hand evaluator)]] - document - docs/obsidian/Reference/Dependencies.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Architecture_Decisions_&_Core_Concepts
SORT file.name ASC
```
