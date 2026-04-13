"""
Model training script.

Usage:
    python train.py
    python train.py --data-dir data/augmented --epochs 40 --batch-size 64
    python train.py --compute-stats     # recompute normalization stats first

After training, exports the model to data/models/card_classifier.onnx.
"""

import argparse
import os
import sys
import time

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau

sys.path.insert(0, os.path.dirname(__file__))

from src.common.constants import CARD_LABELS, IDX_TO_LABEL, NUM_CLASSES
from src.recognition.dataset import (
    compute_mean_std,
    load_dataset,
    load_norm_stats,
    make_loaders,
    save_norm_stats,
)
from src.recognition.model import CardClassifier, count_parameters

MODELS_DIR = "data/models"
CHECKPOINT_PATH = os.path.join(MODELS_DIR, "card_classifier.pt")
ONNX_PATH = os.path.join(MODELS_DIR, "card_classifier.onnx")


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        logits = model(imgs)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * imgs.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        total += imgs.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        logits = model(imgs)
        loss = criterion(logits, labels)
        total_loss += loss.item() * imgs.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        total += imgs.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def print_confusion_summary(model, test_loader, device, top_errors: int = 10):
    """Print the top misclassified pairs on the test set."""
    model.eval()
    from collections import defaultdict
    errors = defaultdict(int)
    for imgs, labels in test_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        preds = model(imgs).argmax(1)
        for true, pred in zip(labels.tolist(), preds.tolist()):
            if true != pred:
                errors[(IDX_TO_LABEL[true], IDX_TO_LABEL[pred])] += 1

    if not errors:
        print("No errors on test set!")
        return

    print(f"\nTop {top_errors} misclassifications (true -> predicted: count):")
    for (true, pred), count in sorted(errors.items(), key=lambda x: -x[1])[:top_errors]:
        print(f"  {true:>6} -> {pred:<6}  ({count})")


def export_onnx(model, path: str, device):
    model.eval()
    dummy = torch.randn(1, 3, 64, 64, device=device)
    torch.onnx.export(
        model,
        dummy,
        path,
        opset_version=17,
        input_names=["image"],
        output_names=["logits"],
        dynamic_axes={"image": {0: "batch"}, "logits": {0: "batch"}},
    )
    print(f"Exported ONNX model -> {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data/augmented")
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--early-stop", type=int, default=5,
                        help="Stop if val loss doesn't improve for N epochs")
    parser.add_argument("--compute-stats", action="store_true",
                        help="Recompute dataset normalization stats before training")
    parser.add_argument("--num-workers", type=int, default=4)
    args = parser.parse_args()

    os.makedirs(MODELS_DIR, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Normalization stats
    norm_stats_path = os.path.join(MODELS_DIR, "norm_stats.json")
    if args.compute_stats or not os.path.exists(norm_stats_path):
        print("Computing dataset normalization stats...")
        mean, std = compute_mean_std(args.data_dir, num_workers=args.num_workers)
        save_norm_stats(mean, std, norm_stats_path)
        print(f"  mean={mean}, std={std}")
    else:
        mean, std = load_norm_stats(norm_stats_path)
        print(f"Loaded norm stats: mean={mean}, std={std}")

    # Datasets
    train_ds, val_ds, test_ds = load_dataset(
        args.data_dir, mean=mean, std=std, augment_train=True,
    )
    train_loader, val_loader, test_loader = make_loaders(
        train_ds, val_ds, test_ds,
        batch_size=args.batch_size, num_workers=args.num_workers,
    )
    print(f"Dataset: {len(train_ds)} train / {len(val_ds)} val / {len(test_ds)} test")

    # Model
    model = CardClassifier(num_classes=NUM_CLASSES, dropout=args.dropout).to(device)
    print(f"Parameters: {count_parameters(model):,}")

    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=args.lr)
    scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=3)

    best_val_loss = float("inf")
    no_improve = 0

    for epoch in range(1, args.epochs + 1):
        t0 = time.time()
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)
        elapsed = time.time() - t0

        print(
            f"Epoch {epoch:3d}/{args.epochs}  "
            f"train loss={train_loss:.4f} acc={train_acc:.4f}  "
            f"val loss={val_loss:.4f} acc={val_acc:.4f}  "
            f"({elapsed:.1f}s)"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            no_improve = 0
            torch.save(model.state_dict(), CHECKPOINT_PATH)
        else:
            no_improve += 1
            if no_improve >= args.early_stop:
                print(f"Early stopping after {epoch} epochs.")
                break

    # Load best weights and evaluate on test set
    model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=device))
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)
    print(f"\nTest accuracy: {test_acc:.4f}  (loss={test_loss:.4f})")

    if test_acc < 0.99:
        print("WARNING: Test accuracy below 99% target. Consider more data or longer training.")
    else:
        print("Target accuracy achieved.")

    print_confusion_summary(model, test_loader, device)
    export_onnx(model, ONNX_PATH, device)


if __name__ == "__main__":
    main()
