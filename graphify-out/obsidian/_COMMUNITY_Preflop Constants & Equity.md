---
type: community
cohesion: 0.10
members: 31
---

# Preflop Constants & Equity

**Cohesion:** 0.10 - loosely connected
**Members:** 31 nodes

## Members
- [[.__init__()_4]] - code - railbird\src\engine\equity.py
- [[.__init__()_5]] - code - railbird\src\engine\lookup.py
- [[._monte_carlo()]] - code - railbird\src\engine\equity.py
- [[._preflop_equity()]] - code - railbird\src\engine\equity.py
- [[.calculate()]] - code - railbird\src\engine\equity.py
- [[.get_equity()]] - code - railbird\src\engine\lookup.py
- [[.hand_class()]] - code - railbird\src\engine\lookup.py
- [[Calculate equity.          Args             hero          List of 2 card label]] - rationale - railbird\src\engine\equity.py
- [[Calculates hero equity given hole cards, board, and opponent count.      Uses pr]] - rationale - railbird\src\engine\equity.py
- [[Canonical card label definitions shared across the entire codebase.  54 classes]] - rationale - railbird\src\common\constants.py
- [[Convert label like 'Ah' to display string like 'A♥'.]] - rationale - railbird\src\common\constants.py
- [[Convert two hole cards to a canonical pre-flop hand class string.     e.g. ('Ah']] - rationale - railbird\src\common\constants.py
- [[Core Monte Carlo loop shared by both backends. Returns equity in 0, 1.      ev]] - rationale - railbird\src\engine\equity.py
- [[Equity calculator.  Strategy   - Pre-flop (no board) Use PreflopTable lookup (]] - rationale - railbird\src\engine\equity.py
- [[EquityCalculator]] - code - railbird\src\engine\equity.py
- [[Fast pre-flop equity lookup by hand class and opponent count.]] - rationale - railbird\src\engine\lookup.py
- [[Look up pre-flop equity for hole cards against num_opponents random hands.]] - rationale - railbird\src\engine\lookup.py
- [[Pre-flop equity lookup table.  Maps the 169 canonical starting hand classes to e]] - rationale - railbird\src\engine\lookup.py
- [[PreflopTable]] - code - railbird\src\engine\lookup.py
- [[Return canonical hand class string, e.g. 'AKs', 'TT', '72o'.]] - rationale - railbird\src\engine\lookup.py
- [[Run Monte Carlo equity simulation using eval7.]] - rationale - railbird\src\engine\equity.py
- [[_classify_strength()]] - code - railbird\src\engine\equity.py
- [[_monte_carlo_eval7()]] - code - railbird\src\engine\equity.py
- [[_monte_carlo_treys()]] - code - railbird\src\engine\equity.py
- [[_run_simulation_loop()]] - code - railbird\src\engine\equity.py
- [[_street_from_board()]] - code - railbird\src\engine\equity.py
- [[canonicalize_preflop()]] - code - railbird\src\common\constants.py
- [[constants.py]] - code - railbird\src\common\constants.py
- [[equity.py]] - code - railbird\src\engine\equity.py
- [[label_to_display()]] - code - railbird\src\common\constants.py
- [[lookup.py]] - code - railbird\src\engine\lookup.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Preflop_Constants_&_Equity
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_HUD Display Layer]]

## Top bridge nodes
- [[PreflopTable]] - degree 13, connects to 1 community
- [[.calculate()]] - degree 8, connects to 1 community
- [[equity.py]] - degree 8, connects to 1 community
- [[label_to_display()]] - degree 3, connects to 1 community