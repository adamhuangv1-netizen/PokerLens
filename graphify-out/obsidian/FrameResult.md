---
source_file: "railbird\src\capture\pipeline.py"
type: "code"
community: "Hand History Database"
location: "L21"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Hand_History_Database
---

# FrameResult

## Connections
- [[.known_labels()]] - `method` [EXTRACTED]
- [[.run_once()]] - `calls` [EXTRACTED]
- [[Args             db        PokerDB instance for recording completed hands.]] - `uses` [INFERRED]
- [[Called by LogTailer when a text-hand is completed.]] - `uses` [INFERRED]
- [[CardRecognizer]] - `uses` [INFERRED]
- [[Group card keys by seat name. seat_1_card_1, seat_1_card_2 - seat_1 ...]] - `uses` [INFERRED]
- [[HandTracker]] - `uses` [INFERRED]
- [[HandTracker — state machine that infers hand progression from card visibility.]] - `uses` [INFERRED]
- [[Mutable state for the current in-progress hand.]] - `uses` [INFERRED]
- [[Output of one capture cycle.]] - `rationale_for` [EXTRACTED]
- [[Process a new FrameResult. Call once per capture cycle.         Automatically re]] - `uses` [INFERRED]
- [[Processes FrameResults and maintains hand state.     Records completed hands to]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]
- [[Write a completed hand record to the database.]] - `uses` [INFERRED]
- [[_HandState]] - `uses` [INFERRED]
- [[pipeline.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/Hand_History_Database