# API documentation

Interactive OpenAPI docs: `http://localhost:8000/docs`.

The FastAPI application registers route modules from `backend/app/api/`.

- `GET /health` — service health
- `GET /api/v1/monitoring/overview` — dashboard metrics
- `GET|POST /api/v1/sources` — list/register source
- `DELETE /api/v1/sources/{source_id}` — remove source
- `GET|POST /api/v1/pipelines` — list/create pipeline
- `PATCH /api/v1/pipelines/{pipeline_id}` — update pipeline
- `POST /api/v1/pipelines/{pipeline_id}/run` — execute bundled sales demo
- `GET /api/v1/runs` — execution history
- `GET /api/v1/monitoring/alerts` — failure summary

This is a deliberately scoped API subset, not the full endpoint matrix in the project specification.
