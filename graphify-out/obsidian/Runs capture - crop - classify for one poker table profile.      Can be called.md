---
source_file: "railbird\src\capture\pipeline.py"
type: "rationale"
community: "Card Recognition Inference"
location: "L44"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# Runs capture -> crop -> classify for one poker table profile.      Can be called

## Connections
- [[CaptureLoop]] - `rationale_for` [EXTRACTED]
- [[CardRecognizer]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Card_Recognition_Inference