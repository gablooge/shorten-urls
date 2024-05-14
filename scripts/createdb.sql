SELECT 'CREATE DATABASE shorten_urls' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'shorten_urls')\gexec
