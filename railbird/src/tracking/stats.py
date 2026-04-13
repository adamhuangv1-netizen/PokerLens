"""
Seat statistics computed from the hand history database.

Stats tracked:
  VPIP  — Voluntarily Put money In Pot
  PFR   — Pre-Flop Raise
  AF    — Aggression Factor (bets+raises / calls)
  hands_played — Total hands the seat was active in
"""

from dataclasses import dataclass

from src.tracking.database import PokerDB


@dataclass
class SeatStats:
    seat: str
    player_name: str
    hands_played: int
    vpip: float       # 0.0 - 1.0
    pfr: float        # 0.0 - 1.0
    af: float         # 0.0+
    avg_reaction_time: float # seconds


def compute_stats(db: PokerDB, seat: str, session_id: int = None) -> SeatStats:
    """
    Compute stats for a seat from the database.
    """
    rows = db.get_seat_hands(seat, session_id)

    hands_played = len(rows)
    player_name = rows[-1].get("player_name", "Unknown") if rows else "Unknown"

    if hands_played == 0:
        return SeatStats(seat=seat, player_name=player_name, hands_played=0, vpip=0.0, pfr=0.0, af=0.0, avg_reaction_time=0.0)

    vpip_count = 0
    pfr_count = 0
    total_bets = 0
    total_calls = 0
    total_time = 0.0
    total_turns = 0

    for r in rows:
        action_bets = r.get("action_bets", 0)
        action_calls = r.get("action_calls", 0)
        action_raises = r.get("action_raises", 0)
        preflop_raise = r.get("preflop_raise", 0)

        # VPIP: any voluntary action
        if action_bets > 0 or action_calls > 0 or action_raises > 0:
            vpip_count += 1
        
        if preflop_raise:
            pfr_count += 1

        total_bets += (action_bets + action_raises)
        total_calls += action_calls
        total_time += r.get("total_thinking_time", 0.0)
        total_turns += r.get("turn_action_count", 0)

    vpip = vpip_count / hands_played
    pfr = pfr_count / hands_played
    af = total_bets / float(total_calls) if total_calls > 0 else float(total_bets)
    avg_reaction_time = total_time / float(total_turns) if total_turns > 0 else 0.0

    return SeatStats(
        seat=seat,
        player_name=player_name,
        hands_played=hands_played,
        vpip=round(vpip, 3),
        pfr=round(pfr, 3),
        af=round(af, 2),
        avg_reaction_time=round(avg_reaction_time, 2),
    )


def compute_all_stats(db: PokerDB, seats: list[str], session_id: int = None) -> dict[str, SeatStats]:
    """Compute stats for all seats. Returns dict keyed by seat name."""
    return {seat: compute_stats(db, seat, session_id) for seat in seats}
