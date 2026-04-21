---
source_file: "railbird\src\tracking\database.py"
type: "code"
community: "Hand History Database"
location: "L37"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Hand_History_Database
---

# PokerDB

## Connections
- [[.__init__()_13]] - `method` [EXTRACTED]
- [[._create_schema()]] - `method` [EXTRACTED]
- [[.close()]] - `method` [EXTRACTED]
- [[.end_session()]] - `method` [EXTRACTED]
- [[.flush()]] - `method` [EXTRACTED]
- [[.get_pending_count()]] - `method` [EXTRACTED]
- [[.get_seat_hands()]] - `method` [EXTRACTED]
- [[.get_total_hands()]] - `method` [EXTRACTED]
- [[.record_hand()]] - `method` [EXTRACTED]
- [[.start_session()]] - `method` [EXTRACTED]
- [[Args             db        PokerDB instance for recording completed hands.]] - `uses` [INFERRED]
- [[Called by LogTailer when a text-hand is completed.]] - `uses` [INFERRED]
- [[Compute stats for a seat from the database.]] - `uses` [INFERRED]
- [[Compute stats for all seats. Returns dict keyed by seat name.]] - `uses` [INFERRED]
- [[Group card keys by seat name. seat_1_card_1, seat_1_card_2 - seat_1 ...]] - `uses` [INFERRED]
- [[HandTracker]] - `uses` [INFERRED]
- [[HandTracker — state machine that infers hand progression from card visibility.]] - `uses` [INFERRED]
- [[Mutable state for the current in-progress hand.]] - `uses` [INFERRED]
- [[Process a new FrameResult. Call once per capture cycle.         Automatically re]] - `uses` [INFERRED]
- [[Processes FrameResults and maintains hand state.     Records completed hands to]] - `uses` [INFERRED]
- [[Seat statistics computed from the hand history database.  Stats tracked   VPIP]] - `uses` [INFERRED]
- [[SeatStats]] - `uses` [INFERRED]
- [[Thread-safe SQLite database for hand history.      Writes are buffered in memory]] - `rationale_for` [EXTRACTED]
- [[Write a completed hand record to the database.]] - `uses` [INFERRED]
- [[_HandState]] - `uses` [INFERRED]
- [[database.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/Hand_History_Database