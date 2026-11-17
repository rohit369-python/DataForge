# Project context

DataPulse is a portfolio demonstration of data ingestion, raw-data preservation, data quality, medallion processing, operational APIs, and analytics-ready outputs. The included executable vertical slice is the e-commerce sales batch pipeline.

## Data ownership
- PostgreSQL: source/pipeline/run metadata (transactional control plane).
- Bronze: original source snapshots; checksum-addressed local files in this demo.
- Silver: standardized Parquet datasets.
- Gold: daily business aggregates and quality report.
- Quarantine: rejected rows preserved for inspection.

## Security boundary
This starter has no user authentication or production secrets manager. Do not expose it to the public internet as-is. Configure a strong secret, TLS, auth/RBAC, secret encryption, backups, and least-privilege roles before deployment.
