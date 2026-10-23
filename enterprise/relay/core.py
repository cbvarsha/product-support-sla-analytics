from datetime import datetime, timedelta, timezone
from enum import Enum
from pydantic import BaseModel, Field

class Priority(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"

SLA_MINUTES = {
    Priority.P1: {"response": 15, "resolution": 240},
    Priority.P2: {"response": 60, "resolution": 480},
    Priority.P3: {"response": 240, "resolution": 1440},
    Priority.P4: {"response": 480, "resolution": 4320},
}

class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3, max_length=5000)
    priority: Priority
    service: str = Field(min_length=1, max_length=100)

class Incident(IncidentCreate):
    id: int
    created_at: datetime
    first_response_at: datetime | None = None
    resolved_at: datetime | None = None
    status: str = "OPEN"
    root_cause: str = "UNCLASSIFIED"

RULES = {
    "AUTHENTICATION": ("login", "password", "sso", "authentication", "token"),
    "NETWORK": ("timeout", "network", "latency", "dns", "connection"),
    "DATABASE": ("database", "sql", "query", "deadlock", "postgres"),
    "DEPLOYMENT": ("release", "deployment", "rollback", "build"),
    "PERFORMANCE": ("slow", "cpu", "memory", "performance"),
}

def classify_root_cause(text: str) -> str:
    value = text.lower()
    for category, keywords in RULES.items():
        if any(keyword in value for keyword in keywords):
            return category
    return "OTHER"

def sla_snapshot(incident: Incident, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    policy = SLA_MINUTES[incident.priority]
    response_due = incident.created_at + timedelta(minutes=policy["response"])
    resolution_due = incident.created_at + timedelta(minutes=policy["resolution"])
    response_breached = (incident.first_response_at or now) > response_due
    resolution_breached = (incident.resolved_at or now) > resolution_due
    remaining = (resolution_due - (incident.resolved_at or now)).total_seconds() / 60
    elapsed = ((incident.resolved_at or now) - incident.created_at).total_seconds() / 60
    risk = round(min(100, max(0, elapsed / policy["resolution"] * 100)), 1)
    return {
        "response_due": response_due,
        "resolution_due": resolution_due,
        "response_breached": response_breached,
        "resolution_breached": resolution_breached,
        "resolution_minutes_remaining": round(remaining, 1),
        "risk_score": risk,
        "at_risk": incident.resolved_at is None and not resolution_breached and risk >= 75,
    }
