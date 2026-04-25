"""
TableProfile — stores card/community/seat region definitions for a poker client.

Regions are stored as percentage offsets from the window's top-left corner
so they remain valid when the window is resized.

JSON format:
{
    "name": "pokerstars_6max",
    "window_title": "PokerStars",
    "window_width": 1200,
    "window_height": 800,
    "hero_cards": [
        {"key": "hero_1", "x_pct": 0.45, "y_pct": 0.80, "w_pct": 0.05, "h_pct": 0.09},
        {"key": "hero_2", "x_pct": 0.51, "y_pct": 0.80, "w_pct": 0.05, "h_pct": 0.09}
    ],
    "community_cards": [
        {"key": "flop_1", ...}, {"key": "flop_2", ...}, {"key": "flop_3", ...},
        {"key": "turn", ...}, {"key": "river", ...}
    ],
    "seat_cards": [
        {"key": "seat_1_card_1", "seat": "seat_1", ...}, ...
    ],
    "pot_region": null
}
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional

import numpy as np


@dataclass
class RegionDef:
    key: str            # e.g. "hero_1", "flop_2", "seat_3_card_1"
    x_pct: float        # left offset as fraction of window width
    y_pct: float        # top offset as fraction of window height
    w_pct: float        # width as fraction of window width
    h_pct: float        # height as fraction of window height
    seat: Optional[str] = None  # e.g. "seat_1" (for seat card regions)

    def to_pixels(self, win_w: int, win_h: int) -> tuple[int, int, int, int]:
        """Convert percentage-based region to absolute pixel bbox (x, y, w, h)."""
        x = int(self.x_pct * win_w)
        y = int(self.y_pct * win_h)
        w = max(1, int(self.w_pct * win_w))
        h = max(1, int(self.h_pct * win_h))
        return x, y, w, h


@dataclass
class TableProfile:
    name: str
    window_title: str
    window_width: int           # reference width at calibration time
    window_height: int          # reference height at calibration time
    hero_cards: list[RegionDef] = field(default_factory=list)
    community_cards: list[RegionDef] = field(default_factory=list)
    seat_cards: list[RegionDef] = field(default_factory=list)
    pot_region: Optional[RegionDef] = None
    to_call_region: Optional[RegionDef] = None

    def all_card_regions(self) -> list[RegionDef]:
        """All regions that produce card images (hero + community + opponents)."""
        return self.hero_cards + self.community_cards + self.seat_cards

    def to_dict(self) -> dict:
        d = asdict(self)
        # asdict handles nested dataclasses cleanly
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "TableProfile":
        hero = [RegionDef(**r) for r in d.get("hero_cards", [])]
        community = [RegionDef(**r) for r in d.get("community_cards", [])]
        seat_cards = [RegionDef(**r) for r in d.get("seat_cards", [])]
        pot = RegionDef(**d["pot_region"]) if d.get("pot_region") else None
        to_call = RegionDef(**d["to_call_region"]) if d.get("to_call_region") else None
        return cls(
            name=d["name"],
            window_title=d["window_title"],
            window_width=d["window_width"],
            window_height=d["window_height"],
            hero_cards=hero,
            community_cards=community,
            seat_cards=seat_cards,
            pot_region=pot,
            to_call_region=to_call,
        )


def save_profile(profile: TableProfile, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(profile.to_dict(), f, indent=2)


def load_profile(path: str) -> TableProfile:
    with open(path) as f:
        return TableProfile.from_dict(json.load(f))


def crop_regions(
    frame: np.ndarray,
    profile: TableProfile,
    regions: Optional[list[RegionDef]] = None,
) -> dict[str, np.ndarray]:
    """
    Crop all card regions from a frame captured at the window's current size.

    Args:
        frame: BGR numpy array of the full poker window.
        profile: TableProfile with region definitions.
        regions: If provided, only crop these regions. Default: all card regions.

    Returns:
        Dict mapping region key -> cropped BGR numpy array.
    """
    h, w = frame.shape[:2]
    regions = regions if regions is not None else profile.all_card_regions()
    crops = {}
    for r in regions:
        x, y, rw, rh = r.to_pixels(w, h)
        # Clamp to frame bounds
        x = max(0, min(x, w - 1))
        y = max(0, min(y, h - 1))
        x2 = min(x + rw, w)
        y2 = min(y + rh, h)
        crop = frame[y:y2, x:x2]
        if crop.size > 0:
            crops[r.key] = crop
    return crops
