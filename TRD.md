# TRD

## Architecture
Browser -> FastAPI -> image validation -> persisted classifier -> compliance result -> SQLite.

Restricted-zone events use a deterministic rule engine and are stored in the same incident log.

## Stack
Python, FastAPI, Pillow, scikit-learn, SQLite, HTML, CSS and JavaScript.

## API
GET /api/health
GET /api/metrics
POST /api/predict
POST /api/zone-event
POST /api/incidents
GET /api/incidents

## Testing
Held-out test set, stress test with image perturbations, API smoke tests and invalid-input validation.
