# Architecture

DataPulse uses a modular-monolith control plane (FastAPI) and an independently callable batch data engine. React is the operator UI. PostgreSQL owns operational metadata. The local batch demonstration preserves the input in Bronze, writes cleaned Parquet to Silver, business aggregates to Gold, and invalid rows to Quarantine.

```mermaid
flowchart LR
 A[CSV / API / DB sources] --> B[FastAPI + Data Engine]
 B --> C[Bronze raw snapshots]
 C --> D[Validation + Pandas transforms]
 D --> E[Silver Parquet]
 E --> F[Gold aggregates / PostgreSQL warehouse]
 F --> G[Power BI]
 H[React UI] <--> I[FastAPI]
 I <--> J[(PostgreSQL metadata)]
 K[Airflow optional] --> B
```

Airflow, Kafka, Spark, dbt, MinIO and Redis are extension points or optional profiles; the included demo does not pretend to configure their production-grade integrations.
