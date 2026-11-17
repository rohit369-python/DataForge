"""Small reusable file extractors used by the local demo."""
from pathlib import Path
import pandas as pd
def read_file(path:Path)->pd.DataFrame:
    suffix=path.suffix.lower()
    if suffix==".csv": return pd.read_csv(path)
    if suffix in (".xlsx",".xls"): return pd.read_excel(path)
    if suffix==".json": return pd.read_json(path)
    raise ValueError(f"Unsupported file type: {suffix}")
