--Table Creation DDL
--DIM Table
-- 1.Province Table
create table if not exists dim_province(
	province_id text
	, province_name text
	, primary key(province_id)
);
-- 2.District Table
create table if not exists dim_district(
	district_id text
	, province_id text
	, district_name text
	, primary key(district_id)
	, foreign key(province_id) references dim_province(province_id)
);
-- 3.Case Table
create table if not exists dim_case(
	case_id serial
	, status_name text -- SUSPECT, CLOSECONTACT, PROBABLE, CONFIRMATION
	, status_detail text -- suspect_diisolasi, suspect_discarded, closecontact_dikarantina, closecontact_discarded, probable_diisolasi, probable_diisolasi, confirmation_sembuh,confirmation_meninggal, suspect_meninggal, closecontact_meninggal, probable_meninggal
	, primary key(case_id)
);
--Fact Table
--1. Province Daily table
create table if not exists fact_province_daily(
	id serial
	, province_id text
	, case_id int
	, date text
	, total bigint
	, primary key(id)
	, foreign key(province_id) references dim_province(province_id)
	, foreign key(case_id) references dim_case(case_id)
);

--2. Province Monthly table
create table if not exists fact_province_monthly(
	id serial
	, province_id text
	, case_id int
	, month text
	, total bigint
	, primary key(id)
	, foreign key(province_id) references dim_province(province_id)
	, foreign key(case_id) references dim_case(case_id)
);

--3. Province Yearly table
create table if not exists fact_province_yearly(
	id serial
	, province_id text
	, case_id int
	, year text
	, total bigint
	, primary key(id)
	, foreign key(province_id) references dim_province(province_id)
	, foreign key(case_id) references dim_case(case_id)
);

--4. District Monthly table
create table if not exists fact_district_monthly(
	id serial
	, district_id text
	, case_id int
	, month text
	, total bigint
	, primary key(id)
	, foreign key(district_id) references dim_district(district_id)
	, foreign key(case_id) references dim_case(case_id)
);

--5. District Yearly table
create table if not exists fact_district_yearly(
	id serial
	, district_id text
	, case_id int
	, year text
	, total bigint
	, primary key(id)
	, foreign key(district_id) references dim_district(district_id)
	, foreign key(case_id) references dim_case(case_id)
);

--6. Temporary Fact Table for pre inserting to actual fact table porpose
create table if not exists temp_fact(
	province_id text
	, district_id text
	, "date" date
	, "case" text
	, total bigint
);