---
source_file: "railbird\src\capture\pipeline.py"
type: "rationale"
community: "Card Recognition Inference"
location: "L67"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# Find the poker window if we don't have a handle yet. Returns True if found.

## Connections
- [[._ensure_window()]] - `rationale_for` [EXTRACTED]
- [[CardRecognizer]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Card_Recognition_Inference