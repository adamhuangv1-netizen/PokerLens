---
type: community
cohesion: 0.20
members: 12
---

# Window Capture

**Cohesion:** 0.20 - loosely connected
**Members:** 12 nodes

## Members
- [[Capture a window's current on-screen position.      NOTE mss captures the scree]] - rationale - railbird\src\capture\window.py
- [[Find the first visible window whose title contains `title_substring` (case-insen]] - rationale - railbird\src\capture\window.py
- [[Return all visible windows with non-empty titles and positive dimensions.      A]] - rationale - railbird\src\capture\window.py
- [[Return all visible windows with non-empty titles.]] - rationale - railbird\src\capture\window.py
- [[Return current (left, top, width, height) for a window handle.]] - rationale - railbird\src\capture\window.py
- [[Window discovery and capture utilities (Windows-specific).  Finds a poker client]] - rationale - railbird\src\capture\window.py
- [[_enumerate_windows()]] - code - railbird\src\capture\window.py
- [[capture_window()]] - code - railbird\src\capture\window.py
- [[find_window()]] - code - railbird\src\capture\window.py
- [[get_window_bbox()]] - code - railbird\src\capture\window.py
- [[list_windows()]] - code - railbird\src\capture\window.py
- [[window.py]] - code - railbird\src\capture\window.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Window_Capture
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Card Recognition Inference]]
- 2 edges to [[_COMMUNITY_Table Calibration]]
- 1 edge to [[_COMMUNITY_Training Data Collector]]

## Top bridge nodes
- [[capture_window()]] - degree 5, connects to 3 communities
- [[find_window()]] - degree 5, connects to 2 communities
- [[get_window_bbox()]] - degree 3, connects to 1 community