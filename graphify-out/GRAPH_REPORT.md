# Graph Report - C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens  (2026-04-25)

## Corpus Check
- 38 files · ~2,885,878 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 439 nodes · 866 edges · 37 communities detected
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 374 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]

## God Nodes (most connected - your core abstractions)
1. `PokerDB` - 49 edges
2. `TableProfile` - 46 edges
3. `CardRecognizer` - 36 edges
4. `FrameResult` - 35 edges
5. `HandRecord` - 24 edges
6. `PokerLensApp` - 22 edges
7. `OverlayWindow` - 22 edges
8. `CaptureLoop` - 21 edges
9. `EquityResult` - 20 edges
10. `HandTracker` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Per-seat HUD labels displayed near each opponent seat on the overlay.  Shows VPI` --uses--> `SeatStats`  [INFERRED]
  railbird\src\overlay\seat_hud.py → C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens\railbird\src\tracking\stats.py
- `A small label positioned near a seat showing stats.` --uses--> `SeatStats`  [INFERRED]
  railbird\src\overlay\seat_hud.py → C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens\railbird\src\tracking\stats.py
- `Output of one capture cycle.` --uses--> `CardRecognizer`  [INFERRED]
  railbird\src\capture\pipeline.py → C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens\railbird\src\recognition\inference.py
- `Return only regions with confident, non-empty, non-unknown labels.` --uses--> `CardRecognizer`  [INFERRED]
  railbird\src\capture\pipeline.py → C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens\railbird\src\recognition\inference.py
- `Runs capture -> crop -> classify for one poker table profile.      Can be called` --uses--> `CardRecognizer`  [INFERRED]
  railbird\src\capture\pipeline.py → C:\Users\adam2\OneDrive\Desktop\Projects\PokerLens\railbird\src\recognition\inference.py

## Hyperedges (group relationships)
- **Real-Time Poker Overlay Pipeline: Capture -> Recognition -> Engine -> Overlay** — module_capture, module_recognition, module_engine, module_overlay [EXTRACTED 0.98]
- **Equity Calculation: Preflop Lookup + Monte Carlo + eval7/treys** — concept_preflop_lookup, concept_monte_carlo, dep_eval7, dep_treys [EXTRACTED 0.95]
- **CNN Training Stack: torch + torchvision + onnxruntime + Recognition module** — module_recognition, dep_torch, dep_onnxruntime, concept_cnn_54class [EXTRACTED 0.92]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (39): HandRecord, PokerDB, SQLite persistence layer for hand history and opponent stats.  Schema:   session, Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full., Write all pending hand records to the database., Return all hand_seats rows for a seat (optionally filtered by session)., Thread-safe SQLite database for hand history.      Writes are buffered in memory, _count_known_board() (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (24): DuplicateCardError, EquityCalculator, HandTracker, CardRecognizer, Loads an ONNX card classifier and provides fast CPU inference.      Usage:, LogTailer, Watches a directory for the latest hand history file and tails it., CaptureWorker (+16 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (31): Dataset, _AugmentedSubset, compute_mean_std(), get_transforms(), load_dataset(), load_norm_stats(), make_loaders(), Dataset and DataLoader helpers for card classification.  Expects images organize (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.1
Nodes (41): ADR 001: CNN vs YOLO for Card Recognition, Architecture Decision Record (ADR), 54-Class CNN Card Classifier, EquityCalculator, EquityResult Output Type, Hand Tracker State Machine, Heads-Up Display (HUD), Monte Carlo Equity Simulation (+33 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (22): ChipOcr, ChipOcr — reads chip amounts from a cropped screen region.  Designed for poker p, Reads a chip amount from a BGR image region.      Returns None if pytesseract is, Extract a chip amount from a BGR image crop.          Preprocesses: grayscale ->, CaptureLoop — the hot path that runs every frame.  Capture -> Crop -> Classify -, Execute one capture-crop-classify cycle.          Returns a FrameResult. If the, Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence., Output of one capture cycle. (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (25): canonicalize_preflop(), label_to_display(), Canonical card label definitions shared across the entire codebase.  54 classes:, Convert label like 'Ah' to display string like 'A♥'., Convert two hole cards to a canonical pre-flop hand class string.     e.g. ('Ah', _classify_strength(), _monte_carlo_eval7(), _monte_carlo_treys() (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (25): Calibrator, _pct(), Table calibration tool.  Presents a screenshot of the poker window and guides th, Run the calibration UI for the given sequence.          Returns list of RegionDe, Run the calibration UI for the given sequence.          Returns list of RegionDe, Capture the poker window and run the calibration UI.      Returns a saved TableP, Capture the poker window and run the calibration UI.      Returns a saved TableP, Interactive region selection tool using an OpenCV window. (+17 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (25): Convert percentage-based region to absolute pixel bbox (x, y, w, h)., EquityResult, _card_html(), HudPanel, HUD panel — the main info display shown on the overlay.  Shows:   - Hero hole ca, Update all HUD elements. Call from the main GUI thread only., Update all HUD elements. Call from the main GUI thread only., Format a card label as colored HTML text. (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (21): main(), CLI entry point for table calibration.  Usage:     python scripts/calibrate.py -, main(), _next_filename(), Interactive card image collector.  Opens a live view of a screen region and lets, Capture a fullscreen screenshot and let the user drag a crop region., Return next available filename like img_00042.png., Resize frame to 64x64 RGB and save to data/raw/{label}/. Returns saved path. (+13 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (8): benchmark(), ONNX Runtime inference wrapper for card classification.  Provides CardRecognizer, Classify multiple card images in one forward pass.          Args:             im, Print inference latency stats over n random images., BGR uint8 -> normalized float32 tensor (1, 3, 64, 64)., Preprocess a list of BGR images into a batched tensor., Classify a single card image.          Args:             image: BGR numpy array, _softmax()

### Community 10 - "Community 10"
Cohesion: 0.26
Nodes (12): augment_class(), augment_image(), main(), _random_affine(), _random_blur(), _random_brightness_contrast(), _random_crop_resize(), _random_hsv_jitter() (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (6): HandParser, ParsedHand, PlayerAction, Tailer for live poker hand history files (e.g., PokerStars format).  Provides a, Parses standard hand history lines into a ParsedHand object., Parses a single line.          Returns a ParsedHand when the hand finishes (SUMM

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (8): generate_all(), main(), _rank_to_pips(), Generate synthetic raw card images for all 54 classes.  Creates programmatically, Try to load a reasonable font; fall back to PIL default., Render a single card image with slight per-variation noise., render_card(), _try_load_font()

### Community 13 - "Community 13"
Cohesion: 0.32
Nodes (3): Per-seat HUD labels displayed near each opponent seat on the overlay.  Shows VPI, A small label positioned near a seat showing stats., SeatHudLabel

### Community 14 - "Community 14"
Cohesion: 0.6
Nodes (4): crop_grid(), main(), _next_index(), Crop a playing-card grid image into individual labeled training images.  Takes a

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (1): All regions that produce card images (hero + community + opponents).

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (1): Crop all card regions from a frame captured at the window's current size.      A

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (1): Return all visible windows with non-empty titles.

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (1): Capture a window's current on-screen position.      NOTE: mss captures the scree

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (1): Return current (left, top, width, height) for a window handle.

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Convert label like 'Ah' to display string like 'A♥'.

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Convert two hole cards to a canonical pre-flop hand class string.     e.g. ('Ah'

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Thread-safe SQLite database for hand history.      Writes are buffered in memory

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full.

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Write all pending hand records to the database.

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): Return all hand_seats rows for a seat (optionally filtered by session).

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Railbird (Project Codename)

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Seat (Table Position)

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): numpy

## Knowledge Gaps
- **99 isolated node(s):** `Data augmentation pipeline.  Reads images from data/raw/{label}/ and writes augm`, `Apply a random combination of augmentations to one image.`, `Augment all source images for one label to reach `target` total images.     Retu`, `CLI entry point for table calibration.  Usage:     python scripts/calibrate.py -`, `Crop a playing-card grid image into individual labeled training images.  Takes a` (+94 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 15`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `All regions that produce card images (hero + community + opponents).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `Crop all card regions from a frame captured at the window's current size.      A`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `Return all visible windows with non-empty titles.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `Capture a window's current on-screen position.      NOTE: mss captures the scree`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `Return current (left, top, width, height) for a window handle.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `Convert label like 'Ah' to display string like 'A♥'.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `Convert two hole cards to a canonical pre-flop hand class string.     e.g. ('Ah'`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `Thread-safe SQLite database for hand history.      Writes are buffered in memory`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `Write all pending hand records to the database.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `Return all hand_seats rows for a seat (optionally filtered by session).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Railbird (Project Codename)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Seat (Table Position)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `numpy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TableProfile` connect `Community 6` to `Community 0`, `Community 1`, `Community 4`, `Community 7`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `PokerDB` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `evaluate()` connect `Community 2` to `Community 5`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `PokerDB` (e.g. with `CaptureWorker` and `PokerLensApp`) actually correct?**
  _`PokerDB` has 37 INFERRED edges - model-reasoned connections that need verification._
- **Are the 43 inferred relationships involving `TableProfile` (e.g. with `CaptureWorker` and `PokerLensApp`) actually correct?**
  _`TableProfile` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `CardRecognizer` (e.g. with `CaptureWorker` and `PokerLensApp`) actually correct?**
  _`CardRecognizer` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `FrameResult` (e.g. with `CaptureWorker` and `PokerLensApp`) actually correct?**
  _`FrameResult` has 30 INFERRED edges - model-reasoned connections that need verification._