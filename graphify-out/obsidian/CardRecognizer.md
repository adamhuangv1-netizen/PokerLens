---
source_file: "railbird\src\recognition\inference.py"
type: "code"
community: "Card Recognition Inference"
location: "L28"
tags:
  - graphify/code
  - graphify/INFERRED
  - community/Card_Recognition_Inference
---

# CardRecognizer

## Connections
- [[.__init__()_11]] - `method` [EXTRACTED]
- [[._load_norm_stats()]] - `method` [EXTRACTED]
- [[._preprocess()]] - `method` [EXTRACTED]
- [[._preprocess_batch()]] - `method` [EXTRACTED]
- [[.predict()]] - `method` [EXTRACTED]
- [[.predict_batch()]] - `method` [EXTRACTED]
- [[CaptureLoop]] - `uses` [INFERRED]
- [[CaptureLoop — the hot path that runs every frame.  Capture - Crop - Classify -]] - `uses` [INFERRED]
- [[Execute one capture-crop-classify cycle.          Returns a FrameResult. If the]] - `uses` [INFERRED]
- [[Find the poker window if we don't have a handle yet. Returns True if found.]] - `uses` [INFERRED]
- [[FrameResult]] - `uses` [INFERRED]
- [[Loads an ONNX card classifier and provides fast CPU inference.      Usage]] - `rationale_for` [EXTRACTED]
- [[Output of one capture cycle.]] - `uses` [INFERRED]
- [[Return only regions with confident, non-empty, non-unknown labels.]] - `uses` [INFERRED]
- [[Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence.]] - `uses` [INFERRED]
- [[Runs capture - crop - classify for one poker table profile.      Can be called]] - `uses` [INFERRED]
- [[benchmark()]] - `calls` [EXTRACTED]
- [[inference.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/INFERRED #community/Card_Recognition_Inference