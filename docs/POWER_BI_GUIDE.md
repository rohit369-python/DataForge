# Power BI guide

For a quick demonstration, import `data/gold/daily_sales_summary.csv` into Power BI Desktop. For a deployed warehouse, connect to PostgreSQL and use curated Gold views in the `analytics` schema. DAX examples are in `powerbi/dax/measures.dax`. Set relationships from the date dimension to fact date keys; use a marked date table.

Power BI refresh is not automated by this repository. Configure credentials, gateway/cloud connectivity and a scheduled refresh in Power BI Service after publishing.
