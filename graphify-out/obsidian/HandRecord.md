---
source_file: "railbird\src\tracking\database.py"
type: "code"
community: "Hand History Database"
location: "L29"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Hand_History_Database
---

# HandRecord

## Connections
- [[._commit_hand()]] - `calls` [INFERRED]
- [[.on_parsed_hand()]] - `calls` [INFERRED]
- [[Args             db        PokerDB instance for recording completed hands.]] - `uses` [INFERRED]
- [[Called by LogTailer when a text-hand is completed.]] - `uses` [INFERRED]
- [[Group card keys by seat name. seat_1_card_1, seat_1_card_2 - seat_1 ...]] - `uses` [INFERRED]
- [[HandTracker]] - `uses` [INFERRED]
- [[HandTracker — state machine that infers hand progression from card visibility.]] - `uses` [INFERRED]
- [[Mutable state for the current in-progress hand.]] - `uses` [INFERRED]
- [[Process a new FrameResult. Call once per capture cycle.         Automatically re]] - `uses` [INFERRED]
- [[Processes FrameResults and maintains hand state.     Records completed hands to]] - `uses` [INFERRED]
- [[Write a completed hand record to the database.]] - `uses` [INFERRED]
- [[_HandState]] - `uses` [INFERRED]
- [[database.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/Hand_History_Database