import pandas as pd
def assess_sales(df:pd.DataFrame)->dict:
    required={"order_id","customer_id","product_id","order_date","quantity","unit_price","total_amount","region"}
    missing=sorted(required-set(df.columns))
    if missing: raise ValueError(f"Sales schema missing columns: {missing}")
    completeness=round(float(df[list(required)].notna().mean().mean()*100),2) if len(df) else 100.0
    uniqueness=round(float(df["order_id"].nunique()/max(len(df),1)*100),2)
    dates=pd.to_datetime(df["order_date"],errors="coerce")
    validity=round(float(dates.notna().mean()*100),2) if len(df) else 100.0
    score=round((completeness+uniqueness+validity)/3,2)
    return {"score":score,"completeness":completeness,"uniqueness":uniqueness,"validity":validity,"missing_columns":missing,"input_records":len(df)}
