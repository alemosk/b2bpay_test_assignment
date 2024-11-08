#!/bin/bash
until mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e 'select 1;' > /dev/null 2>&1; do
  echo "Waiting for MySQL..."
  sleep 2
done
echo "MySQL is ready!"
exec "$@"
