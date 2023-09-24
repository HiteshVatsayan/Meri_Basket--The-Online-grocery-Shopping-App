
create schema schema1;
CREATE TABLE IF NOT EXISTS `schema1`.`Customer`(
`customer_id` int auto_increment NOT NULL PRIMARY KEY,
`customer_first_name` varchar(100) NULL,
`customer_middle_name` varchar(100) NULL,
`customer_last_name` varchar(100) NULL,
`account_password` varchar(20)NULL,
`address street` varchar(100),
`address city` varchar(100),
`address state` varchar(100),
`address pincode` int,
`contact_number1` varchar(20),
`contact_number2` varchar(20),
`contact_number3` varchar(20),
`email_ID` varchar(100)
);


CREATE TABLE IF NOT EXISTS `schema1`.`RetailStore`(
`retail_id` int auto_increment NOT NULL PRIMARY KEY,
`account_password` varchar(20) NULL,
`store_address street` varchar(100),
`store_address city` varchar(100),
`store_address state` varchar(100),
`store_address pincode` int,
`contact_number` varchar(20),
`email_ID` varchar(100)
);



create table if not exists `schema1`.`Cart`(
`cart_id` int auto_increment not null primary key,
`current_amount` double null,
`cart_cust_id` int NULL,
INDEX `cart_cust_id_idx` (`cart_cust_id` ASC),
CONSTRAINT `cart_cust_id`
	foreign key (`cart_cust_id`)
    references `schema1`.`Customer`(`customer_id`)
    on update cascade
);



create table if not exists `schema1`.`Product`(
`product_id` int auto_increment not null primary key,
`product_name` varchar(100) not null,
`stock` int not null,
`price` double not null,
`rating` int

);

create table if not exists `schema1`.`Category`(
`category_id` int auto_increment not null primary key,
`category_name` varchar(100) not null,
`cat_prod_id` int NULL,
INDEX `cat_prod_id_idx` (`cat_prod_id` ASC),
CONSTRAINT `cat_prod_id`
	foreign key (`cat_prod_id`)
    references `schema1`.`Product`(`product_id`)
);


CREATE TABLE IF NOT EXISTS `schema1`.`Order`(
`order_id` int auto_increment NOT NULL PRIMARY KEY,
`order_date` varchar(50) NULL,
`order_cust_id` int null,
`order_retail_id` int null,
index `order_retail_id_idx` (`order_retail_id` asc),
index `order_cust_id_idx` (`order_cust_id` asc),
CONSTRAINT `order_cust_id`
	foreign key (`order_cust_id`)
    references `schema1`.`Customer`(`customer_id`),
CONSTRAINT `order_retail_id`
	foreign key (`order_retail_id`)
    references `schema1`.`RetailStore`(`retail_id`)

);


CREATE TABLE IF NOT EXISTS `schema1`.`DeliveryAgent`(
`agent_id` int auto_increment NOT NULL PRIMARY KEY,
`agent_first_name` varchar(100) NULL,
`agent_middle_name` varchar(100) NULL,
`agent_last_name` varchar(100) NULL,
`account_password` varchar(20) NULL,
`location street` varchar(100),
`location city` varchar(100),
`location state` varchar(100),
`location pincode` int,
`contact_number` varchar(20),
`rating` int
);

create table if not exists `schema1`.`Delivery`(
`delivery_id` int auto_increment not null primary key,
`delivery_date` varchar(50) null,
`delivery_status` int null,
`agent_id` int NULL,
`order_id` int NUll,
INDEX `agent_id_idx` (`agent_id` ASC),
INDEX `order_id_idx` (`order_id` ASC),
CONSTRAINT `agent_id`
	foreign key (`agent_id`)
    references `schema1`.`DeliveryAgent`(`agent_id`),
CONSTRAINT `order_id`
	foreign key (`order_id`)
    references `schema1`.`Order`(`order_id`)
);

CREATE TABLE IF NOT EXISTS `schema1`.`Payment`(
`payment_id` int auto_increment NOT NULL PRIMARY KEY,
`payment_method` int null,
`payment_amount` double,
`pay_cust_id` int NULL,
`pay_order_id` int NUll,
INDEX `pay_cust_id_idx` (`pay_cust_id` ASC),
INDEX `order_id_idx` (`pay_order_id` ASC),
CONSTRAINT `pay_cust_id`
	foreign key (`pay_cust_id`)
    references `schema1`.`Customer`(`customer_id`),
CONSTRAINT `pay_order_id`
	foreign key (`pay_order_id`)
    references `schema1`.`Order`(`order_id`)
    
);

create table if not exists `schema1`.`Membership`(
`membership_id` int auto_increment not null primary key,
`membership_validity` int null,
`membership_type` int null,
`mem_cust_id` int NULL,
INDEX `mem_cust_id_idx` (`mem_cust_id` ASC),
CONSTRAINT `mem_cust_id`
	foreign key (`mem_cust_id`)
    references `schema1`.`Customer`(`customer_id`)
);

create table if not exists `schema1`.`Items`(
`item_id` int auto_increment not null primary key,
`item_name` varchar(100) null,
`item_quantity` int null,
`effective_price` double null,
`item_cart_id` int null,
`item_prod_id` int null,
`item_order_id` int null,
index `item_order_id_idx` (`item_order_id` asc),
index `item_cart_id_idx` (`item_cart_id` asc),
index `item_prod_id_idx`(`item_prod_id` asc),
constraint `item_order_id`
	foreign key (`item_order_id`)
    references `schema1`.`Order`(`order_id`)
    on update no action,
constraint `item_cart_id`
	foreign key (`item_cart_id`)
    references `schema1`.`Cart`(`cart_id`)
    on update no action,
constraint `item_prod_id`
	foreign key (`item_prod_id`)
    references `schema1`.`Product`(`product_id`)
    on update no action    
);


create table if not exists `schema1`.`Discount`(
`discount_id` int auto_increment not null primary key,
`discount_value` double null,
`discount_type` int null,
`disc_store_id` int null,
`disc_prod_id` int NULL,
INDEX `disc_prod_id_idx` (`disc_prod_id` ASC),
INDEX `disc_store_id_idx` (`disc_store_id` ASC),
CONSTRAINT `disc_prod_id`
	foreign key (`disc_prod_id`)
    references `schema1`.`Product`(`product_id`),
constraint `disc_store_id`
	foreign key (`disc_store_id`)
    references `schema1`.`RetailStore`(`Retail_id`)
    on update no action
);
-- SELECT COUNT(current_amount) FROM schema1.Cart;

-- SELECT * FROM schema1.RetailStore;

-- SELECT retail_id FROM schema1.RetailStore WHERE schema1.RetailStore.retail_id>10;

-- SELECT category_name FROM schema1.Category
-- UNION
-- SELECT product_name FROM schema1.Product;

-- SELECT customer.customer_id,customer.customer_first_name,membership.membership_id
-- FROM schema1.customer
-- JOIN schema1.membership
-- ON customer.customer_id=membership.mem_cust_id;

-- SELECT cart.cart_cust_id FROM schema1.cart WHERE cart.current_amount>5000;

-- SELECT customer.customer_id,customer.customer_first_name
-- FROM schema1.customer
-- WHERE customer.customer_id IN(
-- SELECT cart.cart_cust_id FROM schema1.cart WHERE cart.current_amount>5000
-- );

-- SELECT category.category_id,category.category_name,product.product_id,product.product_name
-- FROM schema1.category
-- JOIN schema1.product
-- ON category.cat_prod_id=product.product_id;

-- SELECT discount.disc_prod_id,discount.disc_store_id,retailstore.contact_number
-- FROM schema1.discount
-- JOIN schema1.retailstore
-- ON discount.disc_store_id=retailstore.retail_id;

