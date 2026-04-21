# Graph Report - railbird/src + docs  (2026-04-21)

## Corpus Check
- 42 files · ~14,667 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 310 nodes · 519 edges · 22 communities detected
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Architecture Decisions & Core Concepts|Architecture Decisions & Core Concepts]]
- [[_COMMUNITY_Hand History Database|Hand History Database]]
- [[_COMMUNITY_Card Recognition Inference|Card Recognition Inference]]
- [[_COMMUNITY_HUD Display Layer|HUD Display Layer]]
- [[_COMMUNITY_Preflop Constants & Equity|Preflop Constants & Equity]]
- [[_COMMUNITY_Table Calibration|Table Calibration]]
- [[_COMMUNITY_CNN Training Dataset|CNN Training Dataset]]
- [[_COMMUNITY_Training Data Collector|Training Data Collector]]
- [[_COMMUNITY_Seat Stats & Player HUD|Seat Stats & Player HUD]]
- [[_COMMUNITY_Log Parsing & Hand Detection|Log Parsing & Hand Detection]]
- [[_COMMUNITY_Window Capture|Window Capture]]
- [[_COMMUNITY_CNN Model Architecture|CNN Model Architecture]]
- [[_COMMUNITY_Package Init|Package Init]]
- [[_COMMUNITY_Capture Package Init|Capture Package Init]]
- [[_COMMUNITY_Common Package Init|Common Package Init]]
- [[_COMMUNITY_Engine Package Init|Engine Package Init]]
- [[_COMMUNITY_Overlay Package Init|Overlay Package Init]]
- [[_COMMUNITY_Recognition Package Init|Recognition Package Init]]
- [[_COMMUNITY_Tracking Package Init|Tracking Package Init]]
- [[_COMMUNITY_Project Codename|Project Codename]]
- [[_COMMUNITY_Seat Concept|Seat Concept]]
- [[_COMMUNITY_NumPy Dependency|NumPy Dependency]]

## God Nodes (most connected - your core abstractions)
1. `PokerDB` - 26 edges
2. `TableProfile` - 23 edges
3. `CardRecognizer` - 18 edges
4. `FrameResult` - 16 edges
5. `EquityResult` - 16 edges
6. `HudPanel` - 14 edges
7. `Recognition Module` - 14 edges
8. `PreflopTable` - 13 edges
9. `Advice` - 13 edges
10. `HandRecord` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Seat statistics computed from the hand history database.  Stats tracked:   VPIP` --uses--> `PokerDB`  [INFERRED]
  railbird\src\tracking\stats.py → railbird\src\tracking\database.py
- `Compute stats for a seat from the database.` --uses--> `PokerDB`  [INFERRED]
  railbird\src\tracking\stats.py → railbird\src\tracking\database.py
- `Compute stats for all seats. Returns dict keyed by seat name.` --uses--> `PokerDB`  [INFERRED]
  railbird\src\tracking\stats.py → railbird\src\tracking\database.py
- `Calibrator` --uses--> `TableProfile`  [INFERRED]
  railbird\src\capture\calibrator.py → railbird\src\capture\cropper.py
- `run_calibration()` --calls--> `find_window()`  [INFERRED]
  railbird\src\capture\calibrator.py → railbird\src\capture\window.py

## Hyperedges (group relationships)
- **Real-Time Poker Overlay Pipeline: Capture -> Recognition -> Engine -> Overlay** — module_capture, module_recognition, module_engine, module_overlay [EXTRACTED 0.98]
- **Equity Calculation: Preflop Lookup + Monte Carlo + eval7/treys** — concept_preflop_lookup, concept_monte_carlo, dep_eval7, dep_treys [EXTRACTED 0.95]
- **CNN Training Stack: torch + torchvision + onnxruntime + Recognition module** — module_recognition, dep_torch, dep_onnxruntime, concept_cnn_54class [EXTRACTED 0.92]

## Communities

### Community 0 - "Architecture Decisions & Core Concepts"
Cohesion: 0.1
Nodes (41): ADR 001: CNN vs YOLO for Card Recognition, Architecture Decision Record (ADR), 54-Class CNN Card Classifier, EquityCalculator, EquityResult Output Type, Hand Tracker State Machine, Heads-Up Display (HUD), Monte Carlo Equity Simulation (+33 more)

### Community 1 - "Hand History Database"
Cohesion: 0.1
Nodes (21): HandRecord, PokerDB, SQLite persistence layer for hand history and opponent stats.  Schema:   session, Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full., Write all pending hand records to the database., Thread-safe SQLite database for hand history.      Writes are buffered in memory, _count_known_board(), _HandState (+13 more)

### Community 2 - "Card Recognition Inference"
Cohesion: 0.08
Nodes (18): benchmark(), CardRecognizer, ONNX Runtime inference wrapper for card classification.  Provides CardRecognizer, Classify multiple card images in one forward pass.          Args:             im, Print inference latency stats over n random images., Loads an ONNX card classifier and provides fast CPU inference.      Usage:, BGR uint8 -> normalized float32 tensor (1, 3, 64, 64)., Preprocess a list of BGR images into a batched tensor. (+10 more)

### Community 3 - "HUD Display Layer"
Cohesion: 0.12
Nodes (23): TableProfile, EquityResult, _card_html(), HudPanel, HUD panel — the main info display shown on the overlay.  Shows:   - Hero hole ca, Update all HUD elements. Call from the main GUI thread only., Format a card label as colored HTML text., Compact HUD bar showing equity and strategic advice.     Designed to be placed a (+15 more)

### Community 4 - "Preflop Constants & Equity"
Cohesion: 0.1
Nodes (21): canonicalize_preflop(), label_to_display(), Canonical card label definitions shared across the entire codebase.  54 classes:, Convert label like 'Ah' to display string like 'A♥'., Convert two hole cards to a canonical pre-flop hand class string.     e.g. ('Ah', _classify_strength(), EquityCalculator, _monte_carlo_eval7() (+13 more)

### Community 5 - "Table Calibration"
Cohesion: 0.13
Nodes (16): Calibrator, _pct(), Table calibration tool.  Presents a screenshot of the poker window and guides th, Run the calibration UI for the given sequence.          Returns list of RegionDe, Capture the poker window and run the calibration UI.      Returns a saved TableP, Interactive region selection tool using an OpenCV window., run_calibration(), crop_regions() (+8 more)

### Community 6 - "CNN Training Dataset"
Cohesion: 0.11
Nodes (12): Dataset, _AugmentedSubset, compute_mean_std(), get_transforms(), load_dataset(), Dataset and DataLoader helpers for card classification.  Expects images organize, Compute per-channel mean and std over the entire dataset.     Call once after au, Wraps ImageFolder and remaps class indices to canonical order. (+4 more)

### Community 7 - "Training Data Collector"
Cohesion: 0.12
Nodes (19): main(), _next_filename(), Interactive card image collector.  Opens a live view of a screen region and lets, Capture a fullscreen screenshot and let the user drag a crop region., Return next available filename like img_00042.png., Resize frame to 64x64 RGB and save to data/raw/{label}/. Returns saved path., Run the interactive collector.      Args:         bbox: (left, top, width, heigh, run_collector() (+11 more)

### Community 8 - "Seat Stats & Player HUD"
Cohesion: 0.16
Nodes (10): Return all hand_seats rows for a seat (optionally filtered by session)., Per-seat HUD labels displayed near each opponent seat on the overlay.  Shows VPI, A small label positioned near a seat showing stats., SeatHudLabel, compute_all_stats(), compute_stats(), Seat statistics computed from the hand history database.  Stats tracked:   VPIP, Compute stats for a seat from the database. (+2 more)

### Community 9 - "Log Parsing & Hand Detection"
Cohesion: 0.17
Nodes (8): HandParser, LogTailer, ParsedHand, PlayerAction, Tailer for live poker hand history files (e.g., PokerStars format).  Provides a, Watches a directory for the latest hand history file and tails it., Parses standard hand history lines into a ParsedHand object., Parses a single line.          Returns a ParsedHand when the hand finishes (SUMM

### Community 10 - "Window Capture"
Cohesion: 0.2
Nodes (11): capture_window(), _enumerate_windows(), find_window(), get_window_bbox(), list_windows(), Window discovery and capture utilities (Windows-specific).  Finds a poker client, Return all visible windows with non-empty titles and positive dimensions.      A, Find the first visible window whose title contains `title_substring` (case-insen (+3 more)

### Community 11 - "CNN Model Architecture"
Cohesion: 0.33
Nodes (2): CardClassifier, CardClassifier CNN — 54-class card recognition model.  Architecture:   3x (Conv2

### Community 12 - "Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Capture Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Common Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Engine Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Overlay Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Recognition Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Tracking Package Init"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Project Codename"
Cohesion: 1.0
Nodes (1): Railbird (Project Codename)

### Community 20 - "Seat Concept"
Cohesion: 1.0
Nodes (1): Seat (Table Position)

### Community 21 - "NumPy Dependency"
Cohesion: 1.0
Nodes (1): numpy

## Knowledge Gaps
- **69 isolated node(s):** `Interactive card image collector.  Opens a live view of a screen region and lets`, `Return next available filename like img_00042.png.`, `Resize frame to 64x64 RGB and save to data/raw/{label}/. Returns saved path.`, `Run the interactive collector.      Args:         bbox: (left, top, width, heigh`, `Capture a fullscreen screenshot and let the user drag a crop region.` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Capture Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Common Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Engine Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Overlay Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Recognition Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tracking Package Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Codename`** (1 nodes): `Railbird (Project Codename)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Seat Concept`** (1 nodes): `Seat (Table Position)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `NumPy Dependency`** (1 nodes): `numpy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TableProfile` connect `HUD Display Layer` to `Hand History Database`, `Card Recognition Inference`, `Table Calibration`?**
  _High betweenness centrality (0.282) - this node is a cross-community bridge._
- **Why does `FrameResult` connect `Hand History Database` to `Card Recognition Inference`, `HUD Display Layer`?**
  _High betweenness centrality (0.224) - this node is a cross-community bridge._
- **Why does `PokerDB` connect `Hand History Database` to `Seat Stats & Player HUD`?**
  _High betweenness centrality (0.173) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `PokerDB` (e.g. with `_HandState` and `HandTracker`) actually correct?**
  _`PokerDB` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `TableProfile` (e.g. with `Calibrator` and `Table calibration tool.  Presents a screenshot of the poker window and guides th`) actually correct?**
  _`TableProfile` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `CardRecognizer` (e.g. with `FrameResult` and `CaptureLoop`) actually correct?**
  _`CardRecognizer` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `FrameResult` (e.g. with `TableProfile` and `CardRecognizer`) actually correct?**
  _`FrameResult` has 12 INFERRED edges - model-reasoned connections that need verification._