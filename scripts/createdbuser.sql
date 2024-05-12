DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'shorten_url_user') THEN

      RAISE NOTICE 'Role "shorten_url_user" already exists. Skipping.';
   ELSE
      CREATE ROLE shorten_url_user LOGIN PASSWORD 'CHANGEME';
      ALTER ROLE shorten_url_user SET client_encoding TO 'utf8';
      ALTER ROLE shorten_url_user SET timezone TO 'Asia/Jakarta';
      ALTER DATABASE shorten_urls OWNER TO shorten_url_user;
      GRANT ALL ON ALL TABLES IN SCHEMA public to shorten_url_user;
      GRANT ALL ON ALL SEQUENCES IN SCHEMA public to shorten_url_user;
      GRANT ALL ON ALL SEQUENCES IN SCHEMA public to shorten_url_user;
   END IF;
END
$do$;
