---
type: community
cohesion: 0.12
members: 21
---

# Training Data Collector

**Cohesion:** 0.12 - loosely connected
**Members:** 21 nodes

## Members
- [[Call once at startup to fix coordinate mismatches caused by DPI scaling.     Mus]] - rationale - railbird\src\capture\screenshot.py
- [[Capture a fullscreen screenshot and let the user drag a crop region.]] - rationale - railbird\src\capture\collector.py
- [[Capture a screen region and return a BGR numpy array.      Args         bbox (]] - rationale - railbird\src\capture\screenshot.py
- [[Capture an entire monitor.      Args         monitor_index 1-based monitor ind]] - rationale - railbird\src\capture\screenshot.py
- [[Interactive card image collector.  Opens a live view of a screen region and lets]] - rationale - railbird\src\capture\collector.py
- [[Resize frame to 64x64 RGB and save to dataraw{label}. Returns saved path.]] - rationale - railbird\src\capture\collector.py
- [[Return metadata for all available monitors.      Returns         List of dicts]] - rationale - railbird\src\capture\screenshot.py
- [[Return next available filename like img_00042.png.]] - rationale - railbird\src\capture\collector.py
- [[Run the interactive collector.      Args         bbox (left, top, width, heigh]] - rationale - railbird\src\capture\collector.py
- [[Screen capture utilities using mss.  NOTE mss returns BGRA on Windows. All func]] - rationale - railbird\src\capture\screenshot.py
- [[_next_filename()]] - code - railbird\src\capture\collector.py
- [[_save_image()]] - code - railbird\src\capture\collector.py
- [[_select_region_interactively()]] - code - railbird\src\capture\collector.py
- [[collector.py]] - code - railbird\src\capture\collector.py
- [[grab_fullscreen()]] - code - railbird\src\capture\screenshot.py
- [[grab_region()]] - code - railbird\src\capture\screenshot.py
- [[list_monitors()]] - code - railbird\src\capture\screenshot.py
- [[main()]] - code - railbird\src\capture\collector.py
- [[run_collector()]] - code - railbird\src\capture\collector.py
- [[screenshot.py]] - code - railbird\src\capture\screenshot.py
- [[set_dpi_aware()]] - code - railbird\src\capture\screenshot.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Training_Data_Collector
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Table Calibration]]
- 1 edge to [[_COMMUNITY_Window Capture]]

## Top bridge nodes
- [[grab_fullscreen()]] - degree 4, connects to 1 community
- [[grab_region()]] - degree 4, connects to 1 community