# Database schema

The operational metadata schema is created automatically by SQLAlchemy on startup. Tables included: `data_sources`, `pipelines`, and `pipeline_runs`. The full enterprise schema in the specification (users/RBAC, versioned pipeline steps, task runs, catalog, lineage, quality rule registry, notifications and audit logs) is not yet implemented.

```mermaid
erDiagram
 DATA_SOURCES ||--o{ PIPELINES : configures
 PIPELINES ||--o{ PIPELINE_RUNS : executes
 DATA_SOURCES { int id PK string name string source_type }
 PIPELINES { int id PK string name int source_id FK bool active }
 PIPELINE_RUNS { int id PK int pipeline_id FK string status int records_processed }
```
