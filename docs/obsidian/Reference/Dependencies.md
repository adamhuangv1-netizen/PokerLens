---
tags: [reference]
---

# Dependencies

From `railbird/requirements.txt`:

| Package | Min Version | Used By |
|---------|-------------|---------|
| `mss` | 9.0.0 | [[Architecture/Modules/Capture\|Capture]] — fast cross-platform screen capture |
| `opencv-python` | 4.8.0 | Capture, Recognition — image processing |
| `numpy` | 1.24.0 | Recognition, Engine — array operations |
| `Pillow` | 10.0.0 | Recognition — image loading/transforms |
| `torch` | 2.0.0 | [[Architecture/Modules/Recognition\|Recognition]] — CNN training |
| `torchvision` | 0.15.0 | Recognition — transforms, pretrained models |
| `onnxruntime` | 1.16.0 | Recognition — fast ONNX inference |
| `eval7` | 0.1.9 | [[Architecture/Modules/Engine\|Engine]] — C-backed hand evaluator (primary) |
| `PyQt6` | 6.5.0 | [[Architecture/Modules/Overlay\|Overlay]] — HUD framework |
| `pynput` | 1.7.0 | Global keyboard/mouse hooks |
| `pygetwindow` | 0.0.9 | Capture — window detection |

Install: `pip install -r railbird/requirements.txt`

### Optional

- `treys` — fallback hand evaluator if `eval7` unavailable (`pip install treys`)
