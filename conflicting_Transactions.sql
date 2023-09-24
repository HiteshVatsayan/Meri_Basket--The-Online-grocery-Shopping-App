use schema1;

-- TRANSACTION 1
START TRANSACTION;
INSERT INTO schema1.order(order_id,order_retail_id,order_cust_id,order_date,order_status) VALUES ('801', '61', '142', '4/23/2023 0:38', '1');
DELETE FROM schema1.category 
WHERE 
schema1.category.category_id=1;


-- TRANSACTION 2
START TRANSACTION;
DELETE FROM schema1.product
WHERE schema1.product.product_id in 
(select schema1.category.cat_prod_id FROM schema1.category WHERE schema1.category.category_id=2);


