"""Optional Airflow DAG: invokes the local demo pipeline in an Airflow worker image that has the project installed."""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG("datapulse_sales_demo", start_date=datetime(2025, 1, 1), schedule=None, catchup=False, tags=["datapulse", "demo"]) as dag:
    run_batch = BashOperator(
        task_id="run_bronze_silver_gold",
        bash_command=(
            "python -c 'from pathlib import Path; "
            "from data_engine.pipeline import run_demo_pipeline; "
            "print(run_demo_pipeline(Path(\"/opt/datapulse/data\"), "
            "Path(\"/opt/datapulse/sample_data/raw/sales.csv\")))'"
        ),
    )
