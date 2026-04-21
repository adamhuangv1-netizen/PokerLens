---
source_file: "railbird\src\tracking\hand_tracker.py"
type: "rationale"
community: "Hand History Database"
location: "L58"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Hand_History_Database
---

# Processes FrameResults and maintains hand state.     Records completed hands to

## Connections
- [[FrameResult]] - `uses` [INFERRED]
- [[HandRecord]] - `uses` [INFERRED]
- [[HandTracker]] - `rationale_for` [EXTRACTED]
- [[PokerDB]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Hand_History_Database