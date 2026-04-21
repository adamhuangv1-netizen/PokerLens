---
type: community
cohesion: 0.16
members: 17
---

# Seat Stats & Player HUD

**Cohesion:** 0.16 - loosely connected
**Members:** 17 nodes

## Members
- [[.__init__()_7]] - code - railbird\src\overlay\seat_hud.py
- [[._show_waiting()]] - code - railbird\src\overlay\seat_hud.py
- [[.clear_stats()]] - code - railbird\src\overlay\seat_hud.py
- [[.get_seat_hands()]] - code - railbird\src\tracking\database.py
- [[.update_stats()]] - code - railbird\src\overlay\seat_hud.py
- [[A small label positioned near a seat showing stats.]] - rationale - railbird\src\overlay\seat_hud.py
- [[Compute stats for a seat from the database.]] - rationale - railbird\src\tracking\stats.py
- [[Compute stats for all seats. Returns dict keyed by seat name.]] - rationale - railbird\src\tracking\stats.py
- [[Per-seat HUD labels displayed near each opponent seat on the overlay.  Shows VPI]] - rationale - railbird\src\overlay\seat_hud.py
- [[Return all hand_seats rows for a seat (optionally filtered by session).]] - rationale - railbird\src\tracking\database.py
- [[Seat statistics computed from the hand history database.  Stats tracked   VPIP]] - rationale - railbird\src\tracking\stats.py
- [[SeatHudLabel]] - code - railbird\src\overlay\seat_hud.py
- [[SeatStats]] - code - railbird\src\tracking\stats.py
- [[compute_all_stats()]] - code - railbird\src\tracking\stats.py
- [[compute_stats()]] - code - railbird\src\tracking\stats.py
- [[seat_hud.py]] - code - railbird\src\overlay\seat_hud.py
- [[stats.py]] - code - railbird\src\tracking\stats.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Seat_Stats_&_Player_HUD
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Hand History Database]]
- 1 edge to [[_COMMUNITY_HUD Display Layer]]

## Top bridge nodes
- [[SeatHudLabel]] - degree 8, connects to 1 community
- [[SeatStats]] - degree 6, connects to 1 community
- [[.get_seat_hands()]] - degree 3, connects to 1 community
- [[Seat statistics computed from the hand history database.  Stats tracked   VPIP]] - degree 2, connects to 1 community
- [[Compute stats for a seat from the database.]] - degree 2, connects to 1 community