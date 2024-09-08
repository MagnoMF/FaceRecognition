CREATE EXTENSION IF NOT EXISTS vector;
create table if not exists pictures(
 picture_id SERIAL PRIMARY KEY,
 picture_vector vector NOT NULL,
 cd_user INT NOT NULL,
 update_time TIME DEFAULT current_time,
 update_date DATE DEFAULT current_date,
 FOREIGN KEY (cd_user) REFERENCES users(cd_user) ON DELETE CASCADE
)
