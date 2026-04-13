# PokerLens

## Project Overview
Python desktop poker overlay (codename "railbird") — CNN card recognition, seat-based tracking, equity engine, PyQt6 HUD.

## Structure
- `railbird/src/capture/` - Screen capture, window detection, card cropping
- `railbird/src/recognition/` - CNN model, dataset, inference
- `railbird/src/engine/` - Equity calculation, preflop lookup, strategy
- `railbird/src/overlay/` - PyQt6 HUD widgets
- `railbird/src/tracking/` - Hand history, player stats, database
- `railbird/scripts/` - Data augmentation, calibration, synthetic card generation
- `railbird/data/` - Training data and models (gitignored except preflop_equity.json)

## Environment
- Windows 11, Python 3.13
- Git email: adam.huang.v1@gmail.com
- Remote: github.com/adamhuangv1-netizen/PokerLens

## Conventions
- Training images and models are excluded from git (see .gitignore)
- `railbird/data/preflop_equity.json` IS committed (lookup table, not training data)
- No linter/formatter/type checker configured yet

## Dependencies
torch, torchvision, opencv-python, numpy, Pillow, mss, PyQt6, eval7, onnxruntime, pynput, pygetwindow
