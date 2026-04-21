---
type: community
cohesion: 0.10
members: 40
---

# Hand History Database

**Cohesion:** 0.10 - loosely connected
**Members:** 40 nodes

## Members
- [[.__init__()_13]] - code - railbird\src\tracking\database.py
- [[.__init__()_14]] - code - railbird\src\tracking\hand_tracker.py
- [[._commit_hand()]] - code - railbird\src\tracking\hand_tracker.py
- [[._create_schema()]] - code - railbird\src\tracking\database.py
- [[.close()]] - code - railbird\src\tracking\database.py
- [[.end_session()]] - code - railbird\src\tracking\database.py
- [[.flush()]] - code - railbird\src\tracking\database.py
- [[.get_pending_count()]] - code - railbird\src\tracking\database.py
- [[.get_total_hands()]] - code - railbird\src\tracking\database.py
- [[.on_parsed_hand()]] - code - railbird\src\tracking\hand_tracker.py
- [[.record_hand()]] - code - railbird\src\tracking\database.py
- [[.start_session()]] - code - railbird\src\tracking\database.py
- [[.update()]] - code - railbird\src\tracking\hand_tracker.py
- [[Args             db        PokerDB instance for recording completed hands.]] - rationale - railbird\src\tracking\hand_tracker.py
- [[Called by LogTailer when a text-hand is completed.]] - rationale - railbird\src\tracking\hand_tracker.py
- [[FrameResult]] - code - railbird\src\capture\pipeline.py
- [[Group card keys by seat name. seat_1_card_1, seat_1_card_2 - seat_1 ...]] - rationale - railbird\src\tracking\hand_tracker.py
- [[HandRecord]] - code - railbird\src\tracking\database.py
- [[HandTracker]] - code - railbird\src\tracking\hand_tracker.py
- [[HandTracker — state machine that infers hand progression from card visibility.]] - rationale - railbird\src\tracking\hand_tracker.py
- [[Mutable state for the current in-progress hand.]] - rationale - railbird\src\tracking\hand_tracker.py
- [[PokerDB]] - code - railbird\src\tracking\database.py
- [[Process a new FrameResult. Call once per capture cycle.         Automatically re]] - rationale - railbird\src\tracking\hand_tracker.py
- [[Processes FrameResults and maintains hand state.     Records completed hands to]] - rationale - railbird\src\tracking\hand_tracker.py
- [[Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full.]] - rationale - railbird\src\tracking\database.py
- [[SQLite persistence layer for hand history and opponent stats.  Schema   session]] - rationale - railbird\src\tracking\database.py
- [[Thread-safe SQLite database for hand history.      Writes are buffered in memory]] - rationale - railbird\src\tracking\database.py
- [[Write a completed hand record to the database.]] - rationale - railbird\src\tracking\hand_tracker.py
- [[Write all pending hand records to the database.]] - rationale - railbird\src\tracking\database.py
- [[_HandState]] - code - railbird\src\tracking\hand_tracker.py
- [[_count_known_board()]] - code - railbird\src\tracking\hand_tracker.py
- [[_has_hero_cards()]] - code - railbird\src\tracking\hand_tracker.py
- [[_parse_seats()]] - code - railbird\src\tracking\hand_tracker.py
- [[_street_from_count()]] - code - railbird\src\tracking\hand_tracker.py
- [[current_street()]] - code - railbird\src\tracking\hand_tracker.py
- [[database.py]] - code - railbird\src\tracking\database.py
- [[hand_tracker.py]] - code - railbird\src\tracking\hand_tracker.py
- [[in_hand()]] - code - railbird\src\tracking\hand_tracker.py
- [[seat_names()]] - code - railbird\src\tracking\hand_tracker.py
- [[session_id()]] - code - railbird\src\tracking\database.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hand_History_Database
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Card Recognition Inference]]
- 5 edges to [[_COMMUNITY_Seat Stats & Player HUD]]
- 1 edge to [[_COMMUNITY_HUD Display Layer]]
- 1 edge to [[_COMMUNITY_Log Parsing & Hand Detection]]

## Top bridge nodes
- [[FrameResult]] - degree 16, connects to 2 communities
- [[PokerDB]] - degree 26, connects to 1 community
- [[.close()]] - degree 3, connects to 1 community