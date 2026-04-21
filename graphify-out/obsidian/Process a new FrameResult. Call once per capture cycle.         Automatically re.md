---
source_file: "railbird\src\tracking\hand_tracker.py"
type: "rationale"
community: "Hand History Database"
location: "L89"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Hand_History_Database
---

# Process a new FrameResult. Call once per capture cycle.         Automatically re

## Connections
- [[.update()]] - `rationale_for` [EXTRACTED]
- [[FrameResult]] - `uses` [INFERRED]
- [[HandRecord]] - `uses` [INFERRED]
- [[PokerDB]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Hand_History_Database