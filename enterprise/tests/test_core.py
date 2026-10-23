from datetime import datetime, timedelta, timezone
from relay.core import Incident, Priority, classify_root_cause, sla_snapshot

def test_classification():
    assert classify_root_cause("SSO login failure") == "AUTHENTICATION"
    assert classify_root_cause("unknown issue") == "OTHER"

def test_sla_risk_and_breach():
    now = datetime.now(timezone.utc)
    incident = Incident(id=1, title="Outage", description="Service unavailable", service="API",
                        priority=Priority.P1, created_at=now - timedelta(minutes=200))
    snapshot = sla_snapshot(incident, now)
    assert snapshot["at_risk"] is True
    assert snapshot["resolution_breached"] is False
    assert snapshot["response_breached"] is True
    assert sla_snapshot(incident, now + timedelta(minutes=50))["resolution_breached"] is True
