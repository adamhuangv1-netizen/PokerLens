---
type: community
cohesion: 0.12
members: 34
---

# HUD Display Layer

**Cohesion:** 0.12 - loosely connected
**Members:** 34 nodes

## Members
- [[.__init__()_6]] - code - railbird\src\overlay\hud.py
- [[.__init__()_8]] - code - railbird\src\overlay\widget.py
- [[._build_ui()]] - code - railbird\src\overlay\hud.py
- [[.reposition()]] - code - railbird\src\overlay\widget.py
- [[.toggle_visible()]] - code - railbird\src\overlay\widget.py
- [[.update_display()]] - code - railbird\src\overlay\hud.py
- [[.update_display()_1]] - code - railbird\src\overlay\widget.py
- [[Advice]] - code - railbird\src\engine\strategy.py
- [[Compact HUD bar showing equity and strategic advice.     Designed to be placed a]] - rationale - railbird\src\overlay\hud.py
- [[EquityResult]] - code - railbird\src\engine\equity.py
- [[Format a card label as colored HTML text.]] - rationale - railbird\src\overlay\hud.py
- [[Generate a strategic recommendation from an EquityResult.      Args         res]] - rationale - railbird\src\engine\strategy.py
- [[HUD panel — the main info display shown on the overlay.  Shows   - Hero hole ca]] - rationale - railbird\src\overlay\hud.py
- [[HudPanel]] - code - railbird\src\overlay\hud.py
- [[Move and resize the overlay window.]] - rationale - railbird\src\overlay\widget.py
- [[OverlayWindow]] - code - railbird\src\overlay\widget.py
- [[OverlayWindow — the transparent, always-on-top, click-through PyQt6 window.  Key]] - rationale - railbird\src\overlay\widget.py
- [[QLabel]] - code
- [[QSS styles and color constants for the overlay.]] - rationale - railbird\src\overlay\styles.py
- [[QWidget]] - code
- [[Strategy advisor — converts equity into actionable recommendations.  In v1, advi]] - rationale - railbird\src\engine\strategy.py
- [[TableProfile]] - code - railbird\src\capture\cropper.py
- [[Transparent overlay window displaying the HUD.      Must run on the main GUI thr]] - rationale - railbird\src\overlay\widget.py
- [[Update all HUD elements. Call from the main GUI thread only.]] - rationale - railbird\src\overlay\hud.py
- [[Update the HUD. Safe to call from any thread (uses Qt signal).]] - rationale - railbird\src\overlay\widget.py
- [[_card_html()]] - code - railbird\src\overlay\hud.py
- [[_on_display_update()]] - code - railbird\src\overlay\widget.py
- [[advise()]] - code - railbird\src\engine\strategy.py
- [[equity_color()]] - code - railbird\src\overlay\styles.py
- [[hud.py]] - code - railbird\src\overlay\hud.py
- [[strategy.py]] - code - railbird\src\engine\strategy.py
- [[styles.py]] - code - railbird\src\overlay\styles.py
- [[suit_color()]] - code - railbird\src\overlay\styles.py
- [[widget.py]] - code - railbird\src\overlay\widget.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/HUD_Display_Layer
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Table Calibration]]
- 8 edges to [[_COMMUNITY_Card Recognition Inference]]
- 4 edges to [[_COMMUNITY_Preflop Constants & Equity]]
- 1 edge to [[_COMMUNITY_Hand History Database]]
- 1 edge to [[_COMMUNITY_Seat Stats & Player HUD]]

## Top bridge nodes
- [[TableProfile]] - degree 23, connects to 3 communities
- [[EquityResult]] - degree 16, connects to 1 community
- [[_card_html()]] - degree 5, connects to 1 community
- [[QLabel]] - degree 3, connects to 1 community