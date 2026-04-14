---
title: CNN vs YOLO for Card Recognition
date: 2026-04-13
status: decided
modules: [recognition]
---

# 001 — CNN vs YOLO for Card Recognition

## Context

Needed to choose an architecture for recognising playing cards in cropped screen regions. Initial options were a spatial CNN classifier or YOLO-style object detection.

## Decision

**Spatial CNN with 54 output classes.**

54 classes = 52 standard playing cards + `empty` (no card present) + `back` (face-down card).

## Consequences

- Simpler training pipeline — standard image classification, no bounding box labels needed
- Fast inference on fixed-size crops (cropper handles localisation, model handles classification)
- 54-class model scaffolded in `src/recognition/model.py` and `train.py`
- YOLO not needed: card positions are determined by calibrated crop regions, not detection
