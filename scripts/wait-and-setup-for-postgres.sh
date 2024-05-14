#!/bin/sh
# wait-and-setup-for-postgres.sh
status=1
while [ $status -gt 0 ]
do
  # setup database and username
  if [ -n "$DB_ADMIN_PASSWORD" ]; then
    echo "Setup shorten urls db."
    PGPASSWORD=$DB_ADMIN_PASSWORD psql -U $DB_ADMIN_USER -h $DB_ADMIN_HOST -f scripts/createdb.sql
    PGPASSWORD=$DB_ADMIN_PASSWORD psql -U $DB_ADMIN_USER -h $DB_ADMIN_HOST -f scripts/createdbuser.sql
  else
    echo "Skipping setup shorten urls db."
  fi

  # Set default values for DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, and DB_NAME
  DB_USER="${DB_USER:-postgres}"
  DB_PASSWORD="${DB_PASSWORD:-postgres}"
  DB_HOST="${DB_HOST:-localhost}"
  DB_PORT="${DB_PORT:-5432}"
  DB_NAME="${DB_NAME:-postgres}"

  PG_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
  echo $PG_URL

  psql $PG_URL -c "\q" > /dev/null 2>&1
  status=$?
  sleep 1

  echo "Postgres is unavailable - sleeping"
done
echo "Postgres is up - executing command"
