-- clear the table data before inserting whole updated data
truncate dim_province restart identity cascade;
truncate dim_district restart identity cascade;
truncate dim_case restart identity cascade;
truncate fact_province_daily  restart identity cascade;
truncate fact_province_monthly  restart identity cascade;
truncate fact_province_yearly  restart identity cascade;
truncate fact_district_monthly  restart identity cascade;
truncate fact_district_yearly  restart identity cascade;

-- Dim Table data insert
-- insert data for dim case
INSERT INTO dim_case (status_name,status_detail)
	SELECT * FROM temp_dim_case;

-- insert data for dim province
insert into dim_province
	select distinct kode_prov, nama_prov
	from data_warehouse;

-- insert data for dim district
insert into dim_district 
	select distinct kode_kab,kode_prov,nama_kab
	from data_warehouse;

-- insert data to temp_fact for pre processed data before insert to fact table
insert into temp_fact 
	select kode_prov,kode_kab, tanggal::date,
		unnest(array ['suspect_diisolasi','suspect_discarded','suspect_meninggal','closecontact_dikarantina','closecontact_discarded','closecontact_meninggal','probable_diisolasi','probable_discarded','probable_meninggal','confirmation_sembuh','confirmation_meninggal']) as "case"
		, unnest(array [suspect_diisolasi,suspect_discarded,suspect_meninggal,closecontact_dikarantina,closecontact_discarded,closecontact_meninggal,probable_diisolasi,probable_discarded,probable_meninggal,confirmation_sembuh,confirmation_meninggal]) as "count"
from data_warehouse;

-- insert data to fact_province_daily
insert into fact_province_daily(province_id,case_id , "date", total)
	select province_id, dc.case_id, "date", sum(total) as total 
	from temp_fact tf inner join dim_case dc on concat(dc.status_name,'_',dc.status_detail) = tf."case"
	group by province_id, case_id, "date"
	order by province_id, case_id, "date" asc;

-- insert data to fact_province_monthly
insert into fact_province_monthly(province_id,case_id, "month", total)
	select province_id, dc.case_id, to_char(date,'YYYY-MM') as "month", sum(total) as total 
	from temp_fact tf inner join dim_case dc on concat(dc.status_name,'_',dc.status_detail) = tf."case"
	group by province_id, case_id, "month"
	order by province_id, case_id, "month" asc;
	
-- insert data to fact_province_yearly
insert into fact_province_yearly(province_id,case_id, "year", total)
	select province_id, dc.case_id, to_char("date",'YYYY') as "year", sum(total) as total 
	from temp_fact tf inner join dim_case dc on concat(dc.status_name,'_',dc.status_detail) = tf."case"
	group by province_id, case_id, "year"
	order by province_id, case_id, "year" asc;
	
-- insert data to fact_province_monthly
insert into fact_district_monthly(district_id,case_id, "month", total)
	select district_id, dc.case_id, to_char(date,'YYYY-MM') as "month", sum(total) as total 
	from temp_fact tf inner join dim_case dc on concat(dc.status_name,'_',dc.status_detail) = tf."case"
	group by district_id, case_id, "month"
	order by district_id, case_id, "month" asc;
	
-- insert data to fact_province_yearly
insert into fact_district_yearly(district_id,case_id, "year", total)
	select district_id, dc.case_id, to_char("date",'YYYY') as "year", sum(total) as total 
	from temp_fact tf inner join dim_case dc on concat(dc.status_name,'_',dc.status_detail) = tf."case"
	group by district_id, case_id, "year"
	order by district_id, case_id, "year" asc;