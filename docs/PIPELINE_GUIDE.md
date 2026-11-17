# Pipeline guide

1. Start services.
2. Open the UI and register a source (optional for the bundled demo).
3. Create a pipeline.
4. Press Run now.
5. The API executes `data_engine.pipeline.run_demo_pipeline`.
6. Inspect `data/bronze`, `data/silver`, `data/gold`, and `data/quarantine`.

The demo is deterministic over the bundled sample file. Bronze snapshots use a content checksum in the filename to avoid silently overwriting prior input. The run API currently launches the batch synchronously; Airflow is provided as an optional orchestration example.
