# Relay Enterprise — API Foundation

An extensible FastAPI foundation for priority-aware support operations.

## Run

```bash
cd enterprise
python -m pip install -r requirements.txt
uvicorn relay.api:app --reload
```

Open /docs for interactive API documentation.

## Test

```bash
cd enterprise
PYTHONPATH=. pytest tests -q
```

## Architecture

- `relay/core.py`: typed domain models, SLA policy, deterministic risk scoring and rule-based root-cause classification.
- `relay/api.py`: incident lifecycle and operational KPI endpoints.
- `tests/`: SLA boundary and classification tests.

## Important limitations

This is an **enterprise-oriented prototype**, not a production-ready enterprise deployment. Storage is in memory and resets on restart. Risk scoring is deterministic elapsed-time exposure, **not** a trained ML breach predictor. SLA clocks use calendar time, not business hours or pause policies. Authentication, persistence, audit logs, migrations, rate limiting, observability, tenant isolation and model validation are planned.

All incidents and metrics used in demos must be synthetic. Do not load confidential support tickets.
