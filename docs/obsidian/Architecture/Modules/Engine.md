---
module: engine
tags: [module, engine]
---

# Engine

## Purpose

Calculates hero hand equity given recognised cards. Uses a pre-computed lookup table for pre-flop speed, and Monte Carlo simulation (eval7) for post-flop streets.

## Key Files

| File | Role |
|------|------|
| `src/engine/equity.py` | `EquityCalculator` — main public interface |
| `src/engine/lookup.py` | `PreflopTable` — loads and queries `preflop_equity.json` |
| `src/engine/strategy.py` | Strategy recommendations based on equity |
| `railbird/data/preflop_equity.json` | Pre-computed lookup table (committed to git) |
| `railbird/scripts/generate_preflop_table.py` | Script to regenerate the lookup table |

## Equity Strategy

- **Pre-flop:** `PreflopTable` lookup (~0 ms, uses `preflop_equity.json`)
- **Post-flop:** Monte Carlo with `eval7` (~20–40 ms for 5,000 simulations)
- **Fallback:** `treys` library if `eval7` is not installed

## Output

`EquityResult(equity, hand_strength, street, hand_class, simulations)`

`hand_strength` ∈ {`strong`, `medium`, `marginal`, `weak`}

## Dependencies

→ `eval7` (primary evaluator, C-backed)
→ `treys` (fallback evaluator)
→ [[Architecture/Modules/Recognition|Recognition]] (card labels)

## Open Issues

_None recorded._
