create table if not exists users (
	cd_user SERIAL PRIMARY KEY,
	ds_name VARCHAR(50),
	city VARCHAR(50),
	create_date DATE
);
