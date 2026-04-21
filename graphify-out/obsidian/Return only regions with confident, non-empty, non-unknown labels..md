---
source_file: "railbird\src\capture\pipeline.py"
type: "rationale"
community: "Card Recognition Inference"
location: "L38"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# Return only regions with confident, non-empty, non-unknown labels.

## Connections
- [[.known_labels()]] - `rationale_for` [EXTRACTED]
- [[CardRecognizer]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Card_Recognition_Inference