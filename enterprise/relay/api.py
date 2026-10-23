from collections import Counter
from datetime import datetime, timezone
from threading import Lock
from fastapi import FastAPI, HTTPException
from .core import Incident, IncidentCreate, classify_root_cause, sla_snapshot

app = FastAPI(title="Relay Enterprise Support API", version="0.1.0")
_store: dict[int, Incident] = {}
_lock = Lock()
_next_id = 1

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/incidents", response_model=Incident, status_code=201)
def create_incident(payload: IncidentCreate):
    global _next_id
    with _lock:
        incident_id = _next_id
        _next_id += 1
        incident = Incident(**payload.model_dump(), id=incident_id,
                            created_at=datetime.now(timezone.utc),
                            root_cause=classify_root_cause(payload.title + " " + payload.description))
        _store[incident_id] = incident
    return incident

@app.get("/incidents", response_model=list[Incident])
def list_incidents():
    return list(_store.values())

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    incident = _store.get(incident_id)
    if not incident:
        raise HTTPException(404, "Incident not found")
    return {"incident": incident, "sla": sla_snapshot(incident)}

@app.post("/incidents/{incident_id}/respond")
def respond(incident_id: int):
    with _lock:
        incident = _store.get(incident_id)
        if not incident:
            raise HTTPException(404, "Incident not found")
        if incident.first_response_at is None:
            incident.first_response_at = datetime.now(timezone.utc)
        return incident

@app.post("/incidents/{incident_id}/resolve")
def resolve(incident_id: int):
    with _lock:
        incident = _store.get(incident_id)
        if not incident:
            raise HTTPException(404, "Incident not found")
        if incident.resolved_at is None:
            incident.resolved_at = datetime.now(timezone.utc)
            incident.status = "RESOLVED"
        return incident

@app.get("/analytics/overview")
def overview():
    incidents = list(_store.values())
    snapshots = [sla_snapshot(i) for i in incidents]
    return {
        "total": len(incidents),
        "open": sum(i.status == "OPEN" for i in incidents),
        "breached": sum(s["resolution_breached"] for s in snapshots),
        "at_risk": sum(s["at_risk"] for s in snapshots),
        "by_priority": dict(Counter(i.priority.value for i in incidents)),
        "by_root_cause": dict(Counter(i.root_cause for i in incidents)),
    }
