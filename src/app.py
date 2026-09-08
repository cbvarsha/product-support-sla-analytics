from datetime import datetime, timezone

SLA_HOURS={"P1":4,"P2":8,"P3":24,"P4":72}
def remaining_sla(ticket, now=None):
    now=now or datetime.now(timezone.utc); opened=datetime.fromisoformat(ticket["opened_at"])
    elapsed=(now-opened).total_seconds()/3600; remaining=SLA_HOURS[ticket["priority"]]-elapsed
    return {"elapsed_hours":round(elapsed,2),"remaining_hours":round(remaining,2),"breached":remaining<0,"at_risk":0<=remaining<=2}
def classify_root_cause(text):
    labels={"API":["timeout","endpoint","500"],"DATA":["mismatch","missing","duplicate"],"AUTH":["login","token","permission"],"UI":["button","screen","layout"]}
    lowered=text.lower(); scores={k:sum(word in lowered for word in words) for k,words in labels.items()}
    label=max(scores,key=scores.get); return label if scores[label] else "OTHER"
def queue(tickets, now=None):
    enriched=[{**t,"sla":remaining_sla(t,now),"root_cause":classify_root_cause(t["description"])} for t in tickets]
    return sorted(enriched,key=lambda x:(not x["sla"]["breached"],x["sla"]["remaining_hours"]))
