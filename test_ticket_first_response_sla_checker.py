import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check, parse_sla

def row(t, p, mins):
    return {"ticket": t, "priority": p, "first_response_minutes": str(mins)}

class TestFirstResponseSLA(unittest.TestCase):
    def test_breach(self):
        self.assertEqual(check([row("T1", "P1", 30)], {"P1": 15})[0][4], "BREACH")
    def test_ok(self):
        self.assertEqual(check([row("T1", "P1", 10)], {"P1": 15})[0][4], "OK")
    def test_exactly_at_target_ok(self):
        self.assertEqual(check([row("T1", "P1", 15)], {"P1": 15})[0][4], "OK")
    def test_no_sla_for_unknown_priority(self):
        self.assertEqual(check([row("T1", "P9", 10)], {"P1": 15})[0][4], "NO SLA")
    def test_parse_sla(self):
        self.assertEqual(parse_sla("P1=15,P2=60"), {"P1": 15, "P2": 60})
    def test_breaches_first(self):
        r = check([row("A", "P2", 10), row("B", "P2", 90)], {"P2": 60})
        self.assertEqual(r[0][0], "B")
