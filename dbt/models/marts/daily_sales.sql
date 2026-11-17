select order_date, region, count(distinct order_id) as orders, sum(total_amount) as revenue, sum(quantity) as units_sold from {{ ref('stg_sales') }} group by 1,2
