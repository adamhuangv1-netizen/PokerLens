---
module: recognition
tags: [module, recognition]
---

# Recognition

## Purpose

Runs CNN inference on card image crops. Classifies each crop into one of 54 classes: 52 playing cards + `empty` (no card) + `back` (face-down card). Feeds predictions to [[Architecture/Modules/Engine|Engine]].

## Key Files

| File | Role |
|------|------|
| `src/recognition/model.py` | CNN architecture definition |
| `src/recognition/dataset.py` | PyTorch dataset for training images |
| `src/recognition/inference.py` | Loads ONNX model, runs inference on crops |
| `railbird/train.py` | Training script |
| `railbird/scripts/augment.py` | Data augmentation pipeline |
| `railbird/scripts/generate_synthetic_cards.py` | Synthetic training data generation |

## Class Structure

54 output classes:
- 52 standard playing cards (rank + suit, e.g. `Ah`, `Kd`, `2c`)
- `empty` — no card in the region
- `back` — face-down card visible

## Dependencies

→ `torch`, `torchvision` (training)
→ `onnxruntime` (inference)
→ `Pillow`, `opencv-python` (image processing)
→ [[Architecture/Modules/Capture|Capture]] (receives crops)

## Open Issues

_None recorded._
