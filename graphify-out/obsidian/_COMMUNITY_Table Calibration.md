---
type: community
cohesion: 0.13
members: 25
---

# Table Calibration

**Cohesion:** 0.13 - loosely connected
**Members:** 25 nodes

## Members
- [[.__init__()]] - code - railbird\src\capture\calibrator.py
- [[._draw_overlay()]] - code - railbird\src\capture\calibrator.py
- [[._mouse_callback()]] - code - railbird\src\capture\calibrator.py
- [[.all_card_regions()]] - code - railbird\src\capture\cropper.py
- [[.run()]] - code - railbird\src\capture\calibrator.py
- [[.to_dict()]] - code - railbird\src\capture\cropper.py
- [[.to_pixels()]] - code - railbird\src\capture\cropper.py
- [[All regions that produce card images (hero + community + opponents).]] - rationale - railbird\src\capture\cropper.py
- [[Calibrator]] - code - railbird\src\capture\calibrator.py
- [[Capture the poker window and run the calibration UI.      Returns a saved TableP]] - rationale - railbird\src\capture\calibrator.py
- [[Convert percentage-based region to absolute pixel bbox (x, y, w, h).]] - rationale - railbird\src\capture\cropper.py
- [[Crop all card regions from a frame captured at the window's current size.      A]] - rationale - railbird\src\capture\cropper.py
- [[Interactive region selection tool using an OpenCV window.]] - rationale - railbird\src\capture\calibrator.py
- [[RegionDef]] - code - railbird\src\capture\cropper.py
- [[Run the calibration UI for the given sequence.          Returns list of RegionDe]] - rationale - railbird\src\capture\calibrator.py
- [[Table calibration tool.  Presents a screenshot of the poker window and guides th]] - rationale - railbird\src\capture\calibrator.py
- [[TableProfile — stores cardcommunityseat region definitions for a poker client.]] - rationale - railbird\src\capture\cropper.py
- [[_pct()]] - code - railbird\src\capture\calibrator.py
- [[calibrator.py]] - code - railbird\src\capture\calibrator.py
- [[crop_regions()]] - code - railbird\src\capture\cropper.py
- [[cropper.py]] - code - railbird\src\capture\cropper.py
- [[from_dict()]] - code - railbird\src\capture\cropper.py
- [[load_profile()]] - code - railbird\src\capture\cropper.py
- [[run_calibration()]] - code - railbird\src\capture\calibrator.py
- [[save_profile()]] - code - railbird\src\capture\cropper.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Table_Calibration
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_HUD Display Layer]]
- 3 edges to [[_COMMUNITY_Card Recognition Inference]]
- 2 edges to [[_COMMUNITY_Window Capture]]
- 1 edge to [[_COMMUNITY_Training Data Collector]]

## Top bridge nodes
- [[run_calibration()]] - degree 9, connects to 3 communities
- [[Calibrator]] - degree 9, connects to 1 community
- [[.run()]] - degree 8, connects to 1 community
- [[cropper.py]] - degree 7, connects to 1 community
- [[crop_regions()]] - degree 5, connects to 1 community