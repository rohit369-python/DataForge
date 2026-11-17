# Data dictionary

Sales input: `order_id` unique order/business identifier; `customer_id` customer key; `product_id` product key; `order_date` event date; `quantity` units; `unit_price` per-unit price; `discount` discount amount; `total_amount` order amount; `region` sales region.

Gold daily sales: `order_date`, `total_revenue`, `orders`, `units`. Quality report includes score, completeness, uniqueness, validity, input count, accepted count, quarantined count and SHA-256 source checksum.
