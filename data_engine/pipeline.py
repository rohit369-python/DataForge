from pathlib import Path
import json, hashlib, time
import pandas as pd
from data_engine.quality import assess_sales

def run_demo_pipeline(data_dir:Path, source:Path):
    started=time.perf_counter(); data_dir.mkdir(parents=True,exist_ok=True)
    for layer in ("bronze","silver","gold","quarantine"): (data_dir/layer).mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(source)
    raw_bytes=source.read_bytes(); checksum=hashlib.sha256(raw_bytes).hexdigest()
    bronze=data_dir/"bronze"/f"sales_{checksum[:12]}.csv"
    if not bronze.exists(): bronze.write_bytes(raw_bytes)
    report=assess_sales(df)
    df["order_date"]=pd.to_datetime(df["order_date"],errors="coerce",utc=True)
    df["total_amount"]=pd.to_numeric(df["total_amount"],errors="coerce")
    df["quantity"]=pd.to_numeric(df["quantity"],errors="coerce")
    invalid=df[df["order_date"].isna() | df["total_amount"].isna() | (df["quantity"]<=0)].copy()
    valid=df.drop(index=invalid.index).copy()
    valid=valid.drop_duplicates(subset=["order_id"],keep="last")
    valid["region"]=valid["region"].fillna("Unknown").astype(str).str.strip().str.title()
    valid["total_amount"]=valid["total_amount"].clip(lower=0)
    valid.to_parquet(data_dir/"silver"/"sales_clean.parquet",index=False)
    gold=valid.groupby(valid["order_date"].dt.date,as_index=False).agg(total_revenue=("total_amount","sum"),orders=("order_id","nunique"),units=("quantity","sum"))
    gold.to_csv(data_dir/"gold"/"daily_sales_summary.csv",index=False)
    if not invalid.empty: invalid.to_csv(data_dir/"quarantine"/"sales_rejected.csv",index=False)
    (data_dir/"gold"/"quality_report.json").write_text(json.dumps({**report,"accepted_records":len(valid),"quarantined_records":len(invalid),"source_checksum":checksum},indent=2))
    return {"records_extracted":len(df),"records_processed":len(valid),"records_rejected":len(invalid),"duration_seconds":round(time.perf_counter()-started,3)}
