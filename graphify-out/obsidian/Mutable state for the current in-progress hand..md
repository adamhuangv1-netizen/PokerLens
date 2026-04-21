---
source_file: "railbird\src\tracking\hand_tracker.py"
type: "rationale"
community: "Hand History Database"
location: "L28"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Hand_History_Database
---

# Mutable state for the current in-progress hand.

## Connections
- [[FrameResult]] - `uses` [INFERRED]
- [[HandRecord]] - `uses` [INFERRED]
- [[PokerDB]] - `uses` [INFERRED]
- [[_HandState]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Hand_History_Database