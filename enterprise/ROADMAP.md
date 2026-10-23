# Relay Enterprise delivery roadmap

## Phase 1 — API foundation (implemented here)
- Priority-specific response and resolution clocks
- Incident lifecycle endpoints
- Rule-based root-cause tagging
- Deterministic SLA risk flags
- Operational summary metrics and unit tests

## Phase 2 — Persistent platform
- PostgreSQL, Alembic migrations and transactional repositories
- RBAC, OAuth2/OIDC, secure audit history, pagination and filtering
- Configurable business calendars, holidays, SLA pauses and policy versions
- Structured logs, tracing, metrics, rate limiting and secrets management

## Phase 3 — Analytics and ML
- Synthetic incident generator with leakage-safe train/test time split
- Calibrated breach probability model and baseline comparison
- Precision/recall, PR-AUC, calibration and drift monitoring
- Root-cause taxonomy review, multi-label classification and analyst feedback

## Phase 4 — Corporate experience
- React/TypeScript incident workbench, queue filtering and dashboards
- Accessibility, responsive layout, exports and stakeholder reporting
- Docker Compose, CI quality gates, security scans and deployment runbooks

## Acceptance criteria
- SLA edge cases tested: response, resolution, closure, pause, calendar and timezone
- No client data, secrets or credentials committed
- Explicit distinction between synthetic demonstration metrics and real-world results
- Production readiness assessed through security and reliability reviews
