"""
CardClassifier CNN — 54-class card recognition model.

Architecture:
  3x (Conv2d + BatchNorm + ReLU + MaxPool2d)
  Flatten
  Linear(128) + ReLU + Dropout(0.3)
  Linear(54)

Input:  (B, 3, 64, 64)
Output: (B, 54) logits — use softmax for probabilities
"""

import torch
import torch.nn as nn

from src.common.constants import NUM_CLASSES


class CardClassifier(nn.Module):
    def __init__(self, num_classes: int = NUM_CLASSES, dropout: float = 0.3) -> None:
        super().__init__()

        self.features = nn.Sequential(
            # Block 1: 64x64 -> 32x32
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 2: 32x32 -> 16x16
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Block 3: 16x16 -> 8x8
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        # After 3 max-pools: 64 -> 32 -> 16 -> 8, so feature map is 64 * 8 * 8 = 4096
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        return self.classifier(x)


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    model = CardClassifier()
    dummy = torch.randn(1, 3, 64, 64)
    out = model(dummy)
    print(f"Output shape: {out.shape}")
    print(f"Parameters:   {count_parameters(model):,}")
