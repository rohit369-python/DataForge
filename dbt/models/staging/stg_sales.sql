select order_id, customer_id, product_id, order_date::date as order_date, quantity::integer as quantity, total_amount::numeric(12,2) as total_amount, region from {{ source('raw', 'sales') }}
