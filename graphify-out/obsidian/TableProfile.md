---
source_file: "railbird\src\capture\cropper.py"
type: "code"
community: "HUD Display Layer"
location: "L55"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/HUD_Display_Layer
---

# TableProfile

## Connections
- [[.all_card_regions()]] - `method` [EXTRACTED]
- [[.to_dict()]] - `method` [EXTRACTED]
- [[Calibrator]] - `uses` [INFERRED]
- [[Capture the poker window and run the calibration UI.      Returns a saved TableP]] - `uses` [INFERRED]
- [[CaptureLoop]] - `uses` [INFERRED]
- [[CaptureLoop — the hot path that runs every frame.  Capture - Crop - Classify -]] - `uses` [INFERRED]
- [[Execute one capture-crop-classify cycle.          Returns a FrameResult. If the]] - `uses` [INFERRED]
- [[Find the poker window if we don't have a handle yet. Returns True if found.]] - `uses` [INFERRED]
- [[FrameResult]] - `uses` [INFERRED]
- [[Interactive region selection tool using an OpenCV window.]] - `uses` [INFERRED]
- [[Move and resize the overlay window.]] - `uses` [INFERRED]
- [[Output of one capture cycle.]] - `uses` [INFERRED]
- [[OverlayWindow]] - `uses` [INFERRED]
- [[OverlayWindow — the transparent, always-on-top, click-through PyQt6 window.  Key]] - `uses` [INFERRED]
- [[Return only regions with confident, non-empty, non-unknown labels.]] - `uses` [INFERRED]
- [[Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence.]] - `uses` [INFERRED]
- [[Run the calibration UI for the given sequence.          Returns list of RegionDe]] - `uses` [INFERRED]
- [[Runs capture - crop - classify for one poker table profile.      Can be called]] - `uses` [INFERRED]
- [[Table calibration tool.  Presents a screenshot of the poker window and guides th]] - `uses` [INFERRED]
- [[Transparent overlay window displaying the HUD.      Must run on the main GUI thr]] - `uses` [INFERRED]
- [[Update the HUD. Safe to call from any thread (uses Qt signal).]] - `uses` [INFERRED]
- [[cropper.py]] - `contains` [EXTRACTED]
- [[run_calibration()]] - `calls` [INFERRED]

#graphify/code #graphify/INFERRED #community/HUD_Display_Layer