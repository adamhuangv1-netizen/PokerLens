---
tags: [reference]
---

# Glossary

**ADR** — Architecture Decision Record. A note documenting a significant design choice, its context, and consequences. Stored in `Decisions/`.

**back** — CNN class label for a face-down card (card back visible, rank/suit unknown).

**empty** — CNN class label for a seat or board position with no card present.

**equity** — Hero's probability of winning the hand. Expressed as a float in [0, 1]. Computed by [[Architecture/Modules/Engine|Engine]].

**eval7** — C-backed Python poker hand evaluator. Primary backend for Monte Carlo simulations.

**HUD** — Heads-Up Display. The PyQt6 overlay rendered on top of the poker client window.

**Monte Carlo** — Simulation-based equity calculation. Randomly deals remaining cards and counts win/tie/loss outcomes over N trials. Used post-flop (~5,000 simulations).

**PFR** — Pre-Flop Raise percentage. Stat tracked per player in [[Architecture/Modules/Tracking|Tracking]].

**preflop_equity.json** — Pre-computed lookup table mapping hand classes (e.g. `AKs`) to equity values for 1–9 opponents. Lives at `railbird/data/preflop_equity.json`.

**railbird** — Internal codename for the project (a railbird is someone who watches a poker game without playing).

**seat** — A numbered position at the poker table. The overlay tracks 2–9 seats.

**VPIP** — Voluntarily Put money In Pot percentage. Key stat for classifying player aggression. Tracked by [[Architecture/Modules/Tracking|Tracking]].
