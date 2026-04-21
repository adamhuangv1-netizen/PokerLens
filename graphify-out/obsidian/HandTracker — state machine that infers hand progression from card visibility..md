---
source_file: "railbird\src\tracking\hand_tracker.py"
type: "rationale"
community: "Hand History Database"
location: "L1"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Hand_History_Database
---

# HandTracker — state machine that infers hand progression from card visibility.

## Connections
- [[FrameResult]] - `uses` [INFERRED]
- [[HandRecord]] - `uses` [INFERRED]
- [[PokerDB]] - `uses` [INFERRED]
- [[hand_tracker.py]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Hand_History_Database