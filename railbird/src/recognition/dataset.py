"""
Dataset and DataLoader helpers for card classification.

Expects images organized as:
    data/augmented/
        Ah/
            aug_00000.png
            ...
        2c/
            ...
        empty/
            ...
        back/
            ...

The class names from ImageFolder are sorted alphabetically, which does NOT
match our canonical CARD_LABELS order. We remap them so the model output
index always corresponds to LABEL_TO_IDX.
"""

import json
import os
from typing import Optional

import torch
from torch.utils.data import DataLoader, Dataset, Subset, random_split
from torchvision import datasets, transforms

from src.common.constants import CARD_LABELS, LABEL_TO_IDX, NUM_CLASSES

# ImageNet-style defaults as starting point; recalculate with compute_mean_std()
_DEFAULT_MEAN = (0.485, 0.456, 0.406)
_DEFAULT_STD = (0.229, 0.224, 0.225)

NORM_STATS_FILE = "data/models/norm_stats.json"


def get_transforms(mean: tuple = _DEFAULT_MEAN, std: tuple = _DEFAULT_STD,
                   augment: bool = False) -> transforms.Compose:
    """Build image transforms for training or inference."""
    base = [
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ]
    if augment:
        # Light online augmentation on top of the offline pipeline
        base = [
            transforms.Resize((64, 64)),
            transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.1),
            transforms.RandomRotation(degrees=3),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    return transforms.Compose(base)


def load_dataset(
    data_dir: str,
    mean: tuple = _DEFAULT_MEAN,
    std: tuple = _DEFAULT_STD,
    augment_train: bool = True,
    val_split: float = 0.1,
    test_split: float = 0.1,
    seed: int = 42,
) -> tuple[Dataset, Dataset, Dataset]:
    """
    Load the augmented dataset and split into train/val/test.

    Returns:
        (train_dataset, val_dataset, test_dataset)
    """
    full = datasets.ImageFolder(data_dir)

    # Build a class_to_idx remapping so ImageFolder indices match our canonical order
    remap = {full.class_to_idx[label]: LABEL_TO_IDX[label]
             for label in full.classes if label in LABEL_TO_IDX}

    # Wrap with canonical label remapping
    full = _RemappedDataset(full, remap, augment=False, mean=mean, std=std)

    n = len(full)
    n_test = int(n * test_split)
    n_val = int(n * val_split)
    n_train = n - n_test - n_val

    generator = torch.Generator().manual_seed(seed)
    train_ds, val_ds, test_ds = random_split(full, [n_train, n_val, n_test], generator=generator)

    if augment_train:
        train_ds = _AugmentedSubset(train_ds, mean=mean, std=std)

    return train_ds, val_ds, test_ds


def make_loaders(
    train_ds: Dataset,
    val_ds: Dataset,
    test_ds: Dataset,
    batch_size: int = 64,
    num_workers: int = 4,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False,
                             num_workers=num_workers, pin_memory=True)
    return train_loader, val_loader, test_loader


def compute_mean_std(data_dir: str, num_workers: int = 4) -> tuple[tuple, tuple]:
    """
    Compute per-channel mean and std over the entire dataset.
    Call once after augmentation; save result to data/models/norm_stats.json.
    """
    ds = datasets.ImageFolder(data_dir, transform=transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
    ]))
    loader = DataLoader(ds, batch_size=512, num_workers=num_workers)

    mean = torch.zeros(3)
    std = torch.zeros(3)
    n = 0
    for imgs, _ in loader:
        b = imgs.size(0)
        mean += imgs.view(b, 3, -1).mean(2).sum(0)
        std += imgs.view(b, 3, -1).std(2).sum(0)
        n += b

    mean /= n
    std /= n
    return tuple(mean.tolist()), tuple(std.tolist())


def save_norm_stats(mean: tuple, std: tuple, path: str = NORM_STATS_FILE) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump({"mean": list(mean), "std": list(std)}, f)


def load_norm_stats(path: str = NORM_STATS_FILE) -> tuple[tuple, tuple]:
    with open(path) as f:
        d = json.load(f)
    return tuple(d["mean"]), tuple(d["std"])


class _RemappedDataset(Dataset):
    """Wraps ImageFolder and remaps class indices to canonical order."""

    def __init__(self, base: datasets.ImageFolder, remap: dict,
                 augment: bool, mean: tuple, std: tuple) -> None:
        self._base = base
        self._remap = remap
        self._transform = get_transforms(mean, std, augment=augment)

    def __len__(self) -> int:
        return len(self._base)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        img, label = self._base[idx]
        # img is a PIL Image from ImageFolder (no transform applied yet)
        tensor = self._transform(img)
        return tensor, self._remap.get(label, label)


class _AugmentedSubset(Dataset):
    """Wraps a Subset and applies augmentation transforms."""

    def __init__(self, subset: Subset, mean: tuple, std: tuple) -> None:
        self._subset = subset
        self._transform = get_transforms(mean, std, augment=True)

    def __len__(self) -> int:
        return len(self._subset)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        # The underlying _RemappedDataset already applied a non-augmented transform.
        # We need the raw PIL image. Access it through the base ImageFolder.
        subset = self._subset
        dataset = subset.dataset
        real_idx = subset.indices[idx]
        pil_img, label = dataset._base[real_idx]
        tensor = self._transform(pil_img)
        return tensor, dataset._remap.get(label, label)
