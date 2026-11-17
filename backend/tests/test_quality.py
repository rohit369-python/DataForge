import pandas as pd
from data_engine.quality import assess_sales
def test_quality_score_and_duplicate_detection():
    df=pd.DataFrame({"order_id":[1,1],"customer_id":[2,2],"product_id":[3,3],"order_date":["2025-01-01","bad"],"quantity":[1,1],"unit_price":[10,10],"total_amount":[10,10],"region":["north",None]})
    result=assess_sales(df)
    assert result["uniqueness"]==50.0
    assert result["validity"]==50.0
    assert 0 <= result["score"] <= 100
def test_missing_column_fails_fast():
    import pytest
    with pytest.raises(ValueError): assess_sales(pd.DataFrame({"order_id":[1]}))
