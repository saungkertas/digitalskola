
-- menghitung banyaknya order ID pada oodc dimana order_status = delivered (yang terkirim) dan hanya pada bulan 10 di kolom (order_purchase)
select 
	count(order_id)
from 
	olist_orders_dataset_csv oodc 
where 
	1=1
	and order_status ='delivered'
	and date_part('YEAR',order_purchase_timestamp::date) = 2017--10
	
-- distribusi penjualan suatu item dalam tiap tahun
select 
	date_part('YEAR',order_purchase_timestamp::date)
	, count(order_id)
from
	olist_orders_dataset_csv oodc  
where 
	1=1
	and order_status = 'delivered'
 group by 1
 
 -- Join table
 select 
 	customer_id 
 	, payment_type 
 from 
 	olist_orders_dataset_csv oodc 
 join 
 	olist_order_payments_dataset_csv oopdc  
 on 
	oodc.order_id = oopdc.order_id
limit 100
	
	
-- Homework ---------------------------------------------------------------------------
-- Name : Ardhani Rahmadianto
-- Soal no b : Please write a query that show the total of each product category name
select 
	product_category_name
	,count(product_id)
from
	olist_products_dataset_csv opdc
group by 1
order by 2 desc;
---------------------------------------------------------------------------------------

-- Homework ---------------------------------------------------------------------------
-- Name : Ardhani Rahmadianto
-- Soal no c : Please write a query that show the total of credit card payment type
select 
	count(payment_type) as Credit_Card_Payment_Count
from
	olist_order_payments_dataset_csv oopdc 
where
	payment_type = 'credit_card'
-----------------------------------------------------------------------------------
	
-- coba2
--	Most ordered item
select
	product_id 
	,order_item_id 
from 
	olist_order_items_dataset_csv ooidc 
order by order_item_id desc


--Most payment type
-- Homework ---------------------------------------------------------------------------
-- Name : Ardhani Rahmadianto
--Soal no d : Please write a query that show top 3 payment type with the most order item dataset
select
	payment_type  
	, count(order_id)
from 
	olist_order_payments_dataset_csv 
group by payment_type
order by count(order_id) desc
limit 3;
-------------------------------------------------------------------------------------------------

select 
from

--CREATE VIEW product_order_item_payment_type as
select
	product_id 
	, sum(order_item_id) as sum_order_item_id
	, payment_type
from (
	select 
		product_id  
 		, payment_type
 		, order_item_id 
 	from 
 		olist_order_items_dataset_csv ooidc 
 	join
 		olist_order_payments_dataset_csv oopdc  
 	on 
		ooidc.order_id = oopdc.order_id
	order by order_item_id desc
--	limit 100
)a
group by 1,3
order by sum(order_item_id) desc;

select 
	product_id 
	, sum(order_item_id)
from 
	olist_order_items_dataset_csv ooidc
group by 1
order by 2 desc;

-- Homework ---------------------------------------------------------------------------
-- Name : Ardhani Rahmadianto
-- Soal no e : Please write a query that show the sum of payment value from each payment type which installments is greater than 1
select
	a.payment_type
	, count(a.order_id)
--	, sum(a.payment_value)	
from(
	select
		order_id
		, payment_type
		, payment_installments
		, payment_value
	from
		olist_order_payments_dataset_csv oopdc
	where
		payment_installments > 1		
)a	 
group by a.payment_type;

-- Homework ---------------------------------------------------------------------------
-- Name : Ardhani Rahmadianto
-- Soal no e : Please write a query that show the sum of payment value from each payment type which installments is greater than 1
select	
	payment_type
	, sum(payment_value) as sum_payment_value
from
	olist_order_payments_dataset_csv oopdc
where
	payment_installments > 1
group by payment_type;
----------------------------------------------------------------------------------------------------------------------------------

select	
	payment_type
--	, count(order_id)
	, max(payment_installments)
from
	olist_order_payments_dataset_csv oopdc
--where
--	payment_installments > 1
group by payment_type;


select
	payment_type  
	, count(order_id)
from 
	olist_order_payments_dataset_csv 
group by payment_type
order by count(order_id) desc;



-- query1
select
	max(count)
from (
	select
		date_part('YEAR', shipping_limit_date::date) --no 1
		--date_part('MONTH', shipping_limit_date::date) --no 2
		, count(1)
	from 
		olist_order_items_dataset_csv ooidc 
	where 
		1=1
	group by 1
)a

-- query2
select
	min(count)
from (
	select
		date_part('MONTH', shipping_limit_date::date)
		, count(1)
	from 
		olist_order_items_dataset_csv ooidc 
	where 
		1=1
	group by 1
	order by 1
	--limit 5 --No 4
	offset 8 --No 3
)a

-- query3
select
	--min(sum) --no 5,6
	max(sum) --no 7
from (
	select
		payment_type
		, sum(payment_value)
	from (
		select 
			*
		from(
			select 
				order_id 
				, payment_type
				, payment_value 
			from 
				olist_order_payments_dataset_csv oopdc 
			--group by 1,2,3
			--order by 3 desc 
			--offset 2
			--limit 10
		)a
		--where
			--payment_value >= 50 --No 5, No 7
			--(payment_type = 'credit_card' and payment_value > 6000) --no 6
	)b
	group by 1
)c

--No 7, "if we delete group by, order by , offset and limit, and change min(sum) into max(sum) what is the result
-- update no 7 where juga dihapus

--Query 4
select
	payment_type
	, sum(payment_value) -- no 8,9
--	, avg(payment_value)
from(
	select 
		oopdc.order_id 
		, payment_type
		, payment_value 
		, order_purchase_timestamp
	from
		olist_order_payments_dataset_csv oopdc
	left join(
		select
			order_id 
			, order_purchase_timestamp
		from 
			olist_orders_dataset_csv oodc 
		where 
			order_status = 'delivered'
	)a
	on
		oopdc.order_id = a.order_id 
	where 
		1=1
		--and date_part('YEAR',order_purchase_timestamp::date) >= 2017
		and date_part('MONTH',order_purchase_timestamp::date) = 12		
)a
group by 1
offset 3

-- No 9 " what if we change year into MONTH equal to 12"


