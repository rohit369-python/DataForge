from pathlib import Path
import pandas as pd
from data_engine.pipeline import run_demo_pipeline
from backend.app.core.config import settings
def execute_demo():
    return run_demo_pipeline(Path(settings.data_dir), Path("sample_data/raw/sales.csv"))
