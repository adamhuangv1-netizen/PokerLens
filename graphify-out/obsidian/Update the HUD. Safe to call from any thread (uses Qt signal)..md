---
source_file: "railbird\src\overlay\widget.py"
type: "rationale"
community: "HUD Display Layer"
location: "L129"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/HUD_Display_Layer
---

# Update the HUD. Safe to call from any thread (uses Qt signal).

## Connections
- [[.update_display()_1]] - `rationale_for` [EXTRACTED]
- [[Advice]] - `uses` [INFERRED]
- [[EquityResult]] - `uses` [INFERRED]
- [[HudPanel]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/HUD_Display_Layer