---
source_file: "railbird\src\overlay\hud.py"
type: "rationale"
community: "HUD Display Layer"
location: "L107"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/HUD_Display_Layer
---

# Update all HUD elements. Call from the main GUI thread only.

## Connections
- [[.update_display()]] - `rationale_for` [EXTRACTED]
- [[Advice]] - `uses` [INFERRED]
- [[EquityResult]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/HUD_Display_Layer