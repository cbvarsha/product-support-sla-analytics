from datetime import datetime,timezone
from src.app import remaining_sla,classify_root_cause
def test_breach(): assert remaining_sla({"opened_at":"2026-01-01T00:00:00+00:00","priority":"P1"},datetime(2026,1,1,5,tzinfo=timezone.utc))["breached"]
def test_rca(): assert classify_root_cause("API endpoint returned 500 timeout")=="API"
