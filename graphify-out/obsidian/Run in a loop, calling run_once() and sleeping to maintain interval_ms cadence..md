---
source_file: "railbird\src\capture\pipeline.py"
type: "rationale"
community: "Card Recognition Inference"
location: "L135"
tags:
  - graphify/rationale
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence.

## Connections
- [[.run_forever()]] - `rationale_for` [EXTRACTED]
- [[CardRecognizer]] - `uses` [INFERRED]
- [[TableProfile]] - `uses` [INFERRED]

#graphify/rationale #graphify/INFERRED #community/Card_Recognition_Inference