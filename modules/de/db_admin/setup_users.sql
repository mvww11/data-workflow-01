-- create role ds_user_role and assign read-only permissions on public schema
CREATE ROLE ds_user_role;
GRANT CONNECT ON DATABASE companydata TO ds_user_role;
GRANT USAGE ON SCHEMA public TO ds_user_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ds_user_role;

-- create ds_user and assign ds_user_role role to him
CREATE USER ds_user WITH PASSWORD 'ds_user';
GRANT ds_user_role TO ds_user;

--create role mle_user_role and assign all permissions on public schema
CREATE ROLE mle_user_role;
GRANT CONNECT ON DATABASE companydata TO mle_user_role;
GRANT USAGE ON SCHEMA public TO mle_user_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mle_user_role;

-- create mle_user and assign mle_user_role role to him
CREATE USER mle_user WITH PASSWORD 'mle_user';
GRANT mle_user_role TO mle_user;