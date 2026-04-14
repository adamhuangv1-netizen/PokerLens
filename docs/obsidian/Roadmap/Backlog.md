---
tags: [roadmap]
---

# Backlog

## In Progress

_Nothing active — add items here during sessions._

## Pending

- [ ] Complete CNN training pipeline end-to-end
- [ ] Calibrate crop regions for target poker client
- [ ] Build first working HUD prototype
- [ ] Wire equity results into HUD display
- [ ] Add VPIP/PFR stats to Tracking module
- [ ] Test hand tracker state machine

## Done

- [x] Chose CNN architecture (54 classes) over YOLO — see [[Decisions/001-CNN-vs-YOLO]]
- [x] Scaffolded all 6 modules (`capture`, `recognition`, `engine`, `overlay`, `tracking`, `common`)
- [x] Implemented `EquityCalculator` with eval7 + treys fallback
- [x] Generated pre-flop equity lookup table (`preflop_equity.json`)
