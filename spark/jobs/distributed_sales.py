"""PySpark scale-out demonstration; run with spark-submit when PySpark is installed."""
from pyspark.sql import SparkSession, functions as F
spark=SparkSession.builder.appName("DataPulseSalesAggregate").getOrCreate()
df=spark.read.option("header",True).csv("sample_data/raw/sales.csv")
result=df.groupBy("region").agg(F.countDistinct("order_id").alias("orders"),F.sum(F.col("total_amount").cast("double")).alias("revenue"))
result.show(truncate=False)
spark.stop()
