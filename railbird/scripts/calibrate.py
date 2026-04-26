"""
CLI entry point for table calibration.

Usage:
    python scripts/calibrate.py --window "PokerStars" --profile-name "ps_6max"
    python scripts/calibrate.py --window "PokerStars" --profile-name "ps_6max" --seats
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.capture.calibrator_overlay import run_calibration
from src.capture.screenshot import set_dpi_aware

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "..", "config", "site_profiles")


def main():
    parser = argparse.ArgumentParser(description="Calibrate card regions for a poker client")
    parser.add_argument("--window", required=True,
                        help="Substring of the poker window title (e.g. 'PokerStars')")
    parser.add_argument("--profile-name", required=True,
                        help="Name for this profile (e.g. 'ps_6max')")
    parser.add_argument("--output-dir", default=PROFILES_DIR,
                        help="Directory to save the profile JSON")
    parser.add_argument("--seats", action="store_true",
                        help="Also calibrate opponent seat card regions")
    args = parser.parse_args()

    set_dpi_aware()
    profile = run_calibration(
        window_title=args.window,
        profile_name=args.profile_name,
        output_dir=args.output_dir,
        include_seats=args.seats,
    )

    if profile:
        print("\nCalibration complete. You can now run main.py with this profile.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
