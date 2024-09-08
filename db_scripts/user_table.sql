create table if not exists users (
	cd_user SERIAL PRIMARY KEY,
	ds_name VARCHAR(50),
	cd_role INT,
	create_date DATE
);
