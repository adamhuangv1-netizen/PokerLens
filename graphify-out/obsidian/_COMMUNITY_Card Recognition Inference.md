---
type: community
cohesion: 0.08
members: 35
---

# Card Recognition Inference

**Cohesion:** 0.08 - loosely connected
**Members:** 35 nodes

## Members
- [[.__init__()_11]] - code - railbird\src\recognition\inference.py
- [[.__init__()_3]] - code - railbird\src\capture\pipeline.py
- [[._ensure_window()]] - code - railbird\src\capture\pipeline.py
- [[._load_norm_stats()]] - code - railbird\src\recognition\inference.py
- [[._preprocess()]] - code - railbird\src\recognition\inference.py
- [[._preprocess_batch()]] - code - railbird\src\recognition\inference.py
- [[.known_labels()]] - code - railbird\src\capture\pipeline.py
- [[.predict()]] - code - railbird\src\recognition\inference.py
- [[.predict_batch()]] - code - railbird\src\recognition\inference.py
- [[.run_forever()]] - code - railbird\src\capture\pipeline.py
- [[.run_once()]] - code - railbird\src\capture\pipeline.py
- [[.stop()_1]] - code - railbird\src\capture\pipeline.py
- [[BGR uint8 - normalized float32 tensor (1, 3, 64, 64).]] - rationale - railbird\src\recognition\inference.py
- [[CaptureLoop]] - code - railbird\src\capture\pipeline.py
- [[CaptureLoop — the hot path that runs every frame.  Capture - Crop - Classify -]] - rationale - railbird\src\capture\pipeline.py
- [[CardRecognizer]] - code - railbird\src\recognition\inference.py
- [[Classify a single card image.          Args             image BGR numpy array]] - rationale - railbird\src\recognition\inference.py
- [[Classify multiple card images in one forward pass.          Args             im]] - rationale - railbird\src\recognition\inference.py
- [[Execute one capture-crop-classify cycle.          Returns a FrameResult. If the]] - rationale - railbird\src\capture\pipeline.py
- [[Find the poker window if we don't have a handle yet. Returns True if found.]] - rationale - railbird\src\capture\pipeline.py
- [[Loads an ONNX card classifier and provides fast CPU inference.      Usage]] - rationale - railbird\src\recognition\inference.py
- [[ONNX Runtime inference wrapper for card classification.  Provides CardRecognizer]] - rationale - railbird\src\recognition\inference.py
- [[Output of one capture cycle.]] - rationale - railbird\src\capture\pipeline.py
- [[Preprocess a list of BGR images into a batched tensor.]] - rationale - railbird\src\recognition\inference.py
- [[Print inference latency stats over n random images.]] - rationale - railbird\src\recognition\inference.py
- [[Return only regions with confident, non-empty, non-unknown labels.]] - rationale - railbird\src\capture\pipeline.py
- [[Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence.]] - rationale - railbird\src\capture\pipeline.py
- [[Runs capture - crop - classify for one poker table profile.      Can be called]] - rationale - railbird\src\capture\pipeline.py
- [[_softmax()]] - code - railbird\src\recognition\inference.py
- [[benchmark()]] - code - railbird\src\recognition\inference.py
- [[community_cards()]] - code - railbird\src\capture\pipeline.py
- [[confidence_threshold()]] - code - railbird\src\recognition\inference.py
- [[hero_cards()]] - code - railbird\src\capture\pipeline.py
- [[inference.py]] - code - railbird\src\recognition\inference.py
- [[pipeline.py]] - code - railbird\src\capture\pipeline.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Card_Recognition_Inference
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_HUD Display Layer]]
- 5 edges to [[_COMMUNITY_Hand History Database]]
- 3 edges to [[_COMMUNITY_Table Calibration]]
- 3 edges to [[_COMMUNITY_Window Capture]]

## Top bridge nodes
- [[.run_once()]] - degree 8, connects to 3 communities
- [[Output of one capture cycle.]] - degree 3, connects to 2 communities
- [[CardRecognizer]] - degree 18, connects to 1 community
- [[CaptureLoop]] - degree 9, connects to 1 community
- [[.predict()]] - degree 6, connects to 1 community