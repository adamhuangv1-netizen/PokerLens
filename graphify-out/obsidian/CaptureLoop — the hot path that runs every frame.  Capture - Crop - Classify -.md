---
source_file: "railbird\src\capture\pipeline.py"
type: "rationale"
community: "Card Recognition Inference"
location: "L1"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# CaptureLoop — the hot path that runs every frame.  Capture -> Crop -> Classify -

## Connections
- [[CardRecognizer]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]
- [[pipeline.py]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/INFERRED #community/Card_Recognition_Inference