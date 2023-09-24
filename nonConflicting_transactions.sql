use schema1;

START TRANSACTION;
SELECT discount.disc_prod_id,discount.discount_value,discount.disc_store_id,retailstore.contact_number
FROM schema1.discount
JOIN schema1.retailstore
ON discount.disc_store_id=retailstore.retail_id;
COMMIT;




START TRANSACTION;
INSERT INTO schema1.Delivery (delivery_id, agent_id, order_id, delivery_status, delivery_date) VALUES ('801', '100', '222', '0', '2023-04-24 11:27:43');
INSERT INTO delivery_req VALUES ('801', '100', '0', '222');

SELECT delivery_req.deli_id,delivery_req.deli_req,delivery_req.deli_order_id
FROM schema1.delivery_req
WHERE delivery_req.deli_agent_id=100;
COMMIT;




START TRANSACTION;
SELECT customer.customer_id,customer.customer_first_name AS CustomerWithPremiumMembership
FROM schema1.customer
WHERE customer.customer_id IN(
SELECT membership.mem_cust_id FROM schema1.membership WHERE membership.membership_type =2);
COMMIT;




START TRANSACTION;
INSERT INTO schema1.Customer (customer_id, customer_first_name, customer_middle_name, customer_last_name, account_password, address_street, address_city, address_state, address_pincode, contact_number1, contact_number2, contact_number3, email_ID) VALUES ('1001', 'Andrew', 'Jacob', 'Taut', 'LZMBpcWxj1', 'Ruwayana', 'Elmira', 'New York', '14905', '607-392-2543', '459-108-9172', '106-680-0856', 'andrew@ggm.org');
INSERT INTO schema1.membership VALUES (901,2,0,1001);

UPDATE membership
SET membership_type=1
WHERE membership_type=0;

DELETE from customer WHERE customer.customer_id in
(SELECT membership.mem_cust_id 
 WHERE 
 membership.membership_Vality=0)
;
COMMIT;