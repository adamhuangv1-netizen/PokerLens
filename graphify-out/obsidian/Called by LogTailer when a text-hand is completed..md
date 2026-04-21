---
source_file: "railbird\src\tracking\hand_tracker.py"
type: "rationale"
community: "Hand History Database"
location: "L184"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Hand_History_Database
---

# Called by LogTailer when a text-hand is completed.

## Connections
- [[.on_parsed_hand()]] - `rationale_for` [EXTRACTED]
- [[FrameResult]] - `uses` [INFERRED]
- [[HandRecord]] - `uses` [INFERRED]
- [[PokerDB]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Hand_History_Database