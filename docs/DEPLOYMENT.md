# Deployment

Local: copy `.env.example` to `.env`, change secrets, then `docker compose up --build`. For a lighter local run, install `requirements.txt` and start `uvicorn backend.app.main:app --reload`; SQLite is the default without environment overrides.

Production checklist: managed PostgreSQL, TLS reverse proxy, strong JWT/auth implementation, secret manager, encrypted credentials, network segmentation, non-root containers, backups/restore drills, migrations, monitoring, retention policy, rate limiting and vulnerability scanning. AWS/Azure/GCP deployment templates are not included.
