# Obsidian Vault Design — PokerLens

**Date:** 2026-04-13  
**Status:** Approved  
**Scope:** Unified Obsidian knowledge base inside the PokerLens repo

---

## Purpose

A single vault that serves three roles simultaneously:

1. **Dev notebook** — architecture rationale, module notes, debugging context
2. **Project wiki** — structured docs on how the system works, readable by anyone picking up the codebase
3. **AI handoff hub** — structured context for Claude and Antigravity to pick up state between sessions, replacing the ad-hoc `collaboration.md` workflow

---

## Location

`docs/obsidian/` inside the repo, committed to git.

Rationale: AI agents (Claude, Antigravity) can read vault files directly from the working directory. Notes travel with the code and appear in git history alongside the changes they document.

---

## Folder Structure

```
docs/obsidian/
├── Home.md                        ← Dataview dashboard, vault entry point
├── Architecture/
│   ├── Overview.md                ← System diagram, data flow, module map
│   └── Modules/
│       ├── Capture.md
│       ├── Recognition.md
│       ├── Engine.md
│       ├── Overlay.md
│       └── Tracking.md
├── Decisions/                     ← Architecture Decision Records (ADRs)
│   └── 001-CNN-vs-YOLO.md        ← Migrated from collaboration.md
├── Sessions/                      ← Per-session dev logs
├── Roadmap/
│   ├── Backlog.md
│   └── Milestones.md
└── Reference/
    ├── Dependencies.md            ← Populated from requirements.txt
    └── Glossary.md
```

Top-level folders are **type-based** (Decisions, Sessions, Architecture) for clear filing intent. Module filtering is handled via **tags** (`#capture`, `#engine`, etc.) and wikilinks rather than sub-folders, so cross-cutting notes (e.g. a session touching both Recognition and Engine) don't need to be duplicated.

---

## Note Templates

Stored in `docs/obsidian/.obsidian/templates/`. The Templates core plugin is configured to point at this folder.

### ADR (Architecture Decision Record)

```markdown
---
title: 
date: {{date}}
status: open | decided | superseded
modules: []   # pick from: capture, recognition, engine, overlay, tracking
---

## Context

## Decision

## Consequences
```

ADRs use a sequential number prefix (`001-`, `002-`, ...) so they sort chronologically and can be wikilinked predictably (e.g. `[[Decisions/001-CNN-vs-YOLO]]`).

### Session Log

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

### Module Note

Module notes are persistent (not created from template per session). Each lives at `Architecture/Modules/<Name>.md` and is updated in place.

```markdown
---
module: 
tags: [module]
---

## Purpose

## Key files

## Dependencies
<!-- wikilink to related modules -->

## Open issues
```

---

## Home Dashboard

`Home.md` is the vault entry point. It uses Dataview to surface live state:

```markdown
# PokerLens Knowledge Base

## Open Decisions
\```dataview
table date, modules from "Decisions"
where status = "open"
sort date desc
\```

## Recent Sessions
\```dataview
table date from "Sessions"
sort date desc
limit 7
\```

## Modules
[[Architecture/Modules/Capture|Capture]] · [[Architecture/Modules/Recognition|Recognition]] · [[Architecture/Modules/Engine|Engine]] · [[Architecture/Modules/Overlay|Overlay]] · [[Architecture/Modules/Tracking|Tracking]]
```

---

## Obsidian Configuration

`.obsidian/` is committed to git **except** `workspace.json` and `workspace-mobile.json` (these track open tabs and change on every launch — committing them causes constant noise).

**Core plugins enabled:** backlinks, templates, tags, graph view, outgoing links  
**Community plugins:** Dataview (only)  
**Templates folder:** `.obsidian/templates/`

`.gitignore` additions:
```
docs/obsidian/.obsidian/workspace.json
docs/obsidian/.obsidian/workspace-mobile.json
```

---

## Seed Content

The following notes are created and populated on day one:

| File | Content |
|------|---------|
| `Architecture/Overview.md` | System diagram (text), module map, data flow summary |
| `Architecture/Modules/Capture.md` | Purpose, key files from `src/capture/` |
| `Architecture/Modules/Recognition.md` | Purpose, key files from `src/recognition/`, CNN class count |
| `Architecture/Modules/Engine.md` | Purpose, key files from `src/engine/`, equity lookup details |
| `Architecture/Modules/Overlay.md` | Purpose, key files from `src/overlay/` |
| `Architecture/Modules/Tracking.md` | Purpose, key files from `src/tracking/` |
| `Decisions/001-CNN-vs-YOLO.md` | Migrated and formatted from `collaboration.md` |
| `Roadmap/Backlog.md` | Stubbed with known pending work |
| `Reference/Dependencies.md` | Populated from `railbird/requirements.txt` |
| `Reference/Glossary.md` | Key terms: railbird, HUD, equity, ADR, seat, etc. |

---

## Out of Scope

- Claude Code hooks to auto-scaffold session logs (can be added later once vault structure is proven)
- Daily notes plugin (not needed — Session logs serve this purpose)
- Mobile sync configuration
