import unittest
from src.tracking.database import PokerDB, HandRecord
from src.tracking.stats import compute_stats

class TestStats(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite DB
        self.db = PokerDB(":memory:")
        self.session_id = self.db.start_session("TestProfile")

    def tearDown(self):
        self.db.close()

    def test_vpip(self):
        participation = {
            "seat_1": {"player_name": "Alice", "action_calls": 1}, # VPIP = 1
            "seat_2": {"player_name": "Bob", "action_bets": 0, "action_calls": 0, "action_raises": 0} # VPIP = 0
        }
        
        rec = HandRecord(self.session_id, "preflop", [], participation)
        self.db.record_hand(rec)
        self.db.flush()

        stats_alice = compute_stats(self.db, "seat_1", self.session_id)
        stats_bob = compute_stats(self.db, "seat_2", self.session_id)

        self.assertEqual(stats_alice.vpip, 1.0)
        self.assertEqual(stats_bob.vpip, 0.0)

    def test_reaction_time(self):
        participation = {
            "seat_1": {"player_name": "Alice", "total_thinking_time": 10.5, "turn_action_count": 3},
            "seat_2": {"player_name": "Bob", "total_thinking_time": 0.0, "turn_action_count": 0}
        }
        rec = HandRecord(self.session_id, "preflop", [], participation)
        self.db.record_hand(rec)
        self.db.flush()

        stats_alice = compute_stats(self.db, "seat_1", self.session_id)
        stats_bob = compute_stats(self.db, "seat_2", self.session_id)

        self.assertEqual(stats_alice.avg_reaction_time, 3.5) # 10.5 / 3
        self.assertEqual(stats_bob.avg_reaction_time, 0.0)

    def test_pfr_and_af(self):
        participation1 = {
            "seat_1": {"player_name": "Alice", "action_raises": 2, "preflop_raise": True, "action_calls": 1},
        }
        participation2 = {
            "seat_1": {"player_name": "Alice", "action_raises": 0, "action_bets": 2, "action_calls": 0},
        }
        
        self.db.record_hand(HandRecord(self.session_id, "flop", [], participation1))
        self.db.record_hand(HandRecord(self.session_id, "turn", [], participation2))
        self.db.flush()

        stats = compute_stats(self.db, "seat_1", self.session_id)
        
        # 2 hands played
        # Hand 1: raised preflop. Hand 2: did not. PFR = 1 / 2 = 0.5
        self.assertEqual(stats.pfr, 0.5)
        
        # Total bets/raises: 2 + 2 = 4. Total calls: 1. AF = 4 / 1 = 4.0
        self.assertEqual(stats.af, 4.0)

if __name__ == '__main__':
    unittest.main()
