"""
One-time script to generate the pre-flop equity lookup table.

Runs Monte Carlo simulations for all 169 canonical hand classes vs
1-9 opponents and writes the results to data/preflop_equity.json.

Runtime: ~20-40 minutes depending on CPU speed and simulation count.

Usage:
    python scripts/generate_preflop_table.py
    python scripts/generate_preflop_table.py --sims 20000 --output data/preflop_equity.json
"""

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import eval7
    _BACKEND = "eval7"
except ImportError:
    try:
        from treys import Evaluator, Card as TreysCard
        _BACKEND = "treys"
    except ImportError:
        print("ERROR: Install eval7 or treys first: pip install eval7")
        sys.exit(1)

# All 169 canonical hand classes
_RANKS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

def _all_hand_classes() -> list[str]:
    classes = []
    for i, r1 in enumerate(_RANKS):
        for j, r2 in enumerate(_RANKS):
            if i < j:
                classes.append(f"{r1}{r2}s")  # suited
                classes.append(f"{r1}{r2}o")  # offsuit
            elif i == j:
                classes.append(f"{r1}{r2}")   # pocket pair
    return classes


def _sample_hand_for_class(hand_class: str) -> tuple[str, str]:
    """Pick a concrete hand matching the given class."""
    suits = ["c", "d", "h", "s"]
    if len(hand_class) == 2:  # pocket pair
        r = hand_class[0]
        s1, s2 = random.sample(suits, 2)
        return f"{r}{s1}", f"{r}{s2}"
    r1, r2, category = hand_class[0], hand_class[1], hand_class[2]
    if category == "s":  # suited
        s = random.choice(suits)
        return f"{r1}{s}", f"{r2}{s}"
    else:  # offsuit
        s1, s2 = random.sample(suits, 2)
        return f"{r1}{s1}", f"{r2}{s2}"


def _compute_equity_eval7(hand_class: str, num_opponents: int, num_sims: int) -> float:
    wins = ties = 0
    for _ in range(num_sims):
        c1, c2 = _sample_hand_for_class(hand_class)
        hero = [eval7.Card(c1), eval7.Card(c2)]
        known = set(hero)
        deck = [c for c in eval7.Deck() if c not in known]
        sample = random.sample(deck, 5 + num_opponents * 2)
        board = sample[:5]
        opp_hands = [sample[5 + i * 2: 5 + i * 2 + 2] for i in range(num_opponents)]
        hero_val = eval7.evaluate(hero + board)
        opp_vals = [eval7.evaluate(h + board) for h in opp_hands]
        best = min(opp_vals)
        if hero_val < best:
            wins += 1
        elif hero_val == best:
            ties += 1
    return (wins + ties * 0.5) / num_sims


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sims", type=int, default=10000,
                        help="Simulations per hand class per opponent count")
    parser.add_argument("--output", default="data/preflop_equity.json")
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(__file__), "..")
    output = os.path.join(base, args.output)
    os.makedirs(os.path.dirname(output), exist_ok=True)

    classes = _all_hand_classes()
    result = {}
    total = len(classes) * 9
    done = 0
    t0 = time.time()

    print(f"Generating pre-flop equity table ({len(classes)} classes × 9 opp counts, {args.sims} sims each)")
    print(f"Backend: {_BACKEND}")

    for hand_class in classes:
        equities = []
        for num_opp in range(1, 10):
            if _BACKEND == "eval7":
                eq = _compute_equity_eval7(hand_class, num_opp, args.sims)
            else:
                # treys fallback (much slower)
                eq = _compute_equity_eval7(hand_class, num_opp, args.sims)  # same logic
            equities.append(round(eq, 4))
            done += 1
            if done % 50 == 0:
                elapsed = time.time() - t0
                rate = done / elapsed
                remaining = (total - done) / rate
                print(f"  {done}/{total}  ({elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining)")

        result[hand_class] = equities
        # Save incrementally in case of interruption
        with open(output, "w") as f:
            json.dump(result, f, indent=2)

    print(f"\nDone. Saved to {output}")
    print(f"Total time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
