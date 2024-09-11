#!/bin/bash
set -e

# Start MySQL server in the background
docker-entrypoint.sh mysqld &

# Wait for MySQL server to be ready
until mysql -u root -proot_password -e "SELECT 1" > /dev/null 2>&1; do
  echo "Waiting for MySQL server to be ready..."
  sleep 2
done

# Create the database if it doesn't exist
mysql -u root -proot_password -e "CREATE DATABASE IF NOT EXISTS jopmed_dev_db;"

# Source the SQL dump file
mysql -u root -proot_password jopmed_dev_db < /docker-entrypoint-initdb.d/jopmed-dump-prod.sql

# Keep the container running
wait