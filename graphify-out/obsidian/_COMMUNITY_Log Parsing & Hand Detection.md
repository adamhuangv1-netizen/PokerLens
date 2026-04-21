---
type: community
cohesion: 0.17
members: 16
---

# Log Parsing & Hand Detection

**Cohesion:** 0.17 - loosely connected
**Members:** 16 nodes

## Members
- [[.__init__()_1]] - code - railbird\src\capture\log_tailer.py
- [[.__init__()_2]] - code - railbird\src\capture\log_tailer.py
- [[._get_latest_file()]] - code - railbird\src\capture\log_tailer.py
- [[._tail_loop()]] - code - railbird\src\capture\log_tailer.py
- [[.parse_line()]] - code - railbird\src\capture\log_tailer.py
- [[.start()]] - code - railbird\src\capture\log_tailer.py
- [[.stop()]] - code - railbird\src\capture\log_tailer.py
- [[HandParser]] - code - railbird\src\capture\log_tailer.py
- [[LogTailer]] - code - railbird\src\capture\log_tailer.py
- [[ParsedHand]] - code - railbird\src\capture\log_tailer.py
- [[Parses a single line.          Returns a ParsedHand when the hand finishes (SUMM]] - rationale - railbird\src\capture\log_tailer.py
- [[Parses standard hand history lines into a ParsedHand object.]] - rationale - railbird\src\capture\log_tailer.py
- [[PlayerAction]] - code - railbird\src\capture\log_tailer.py
- [[Tailer for live poker hand history files (e.g., PokerStars format).  Provides a]] - rationale - railbird\src\capture\log_tailer.py
- [[Watches a directory for the latest hand history file and tails it.]] - rationale - railbird\src\capture\log_tailer.py
- [[log_tailer.py]] - code - railbird\src\capture\log_tailer.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Log_Parsing_&_Hand_Detection
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Hand History Database]]

## Top bridge nodes
- [[._tail_loop()]] - degree 4, connects to 1 community