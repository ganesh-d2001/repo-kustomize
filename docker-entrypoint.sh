#!/bin/bash

# Start the PostgreSQL service
service postgresql start

# Wait for PostgreSQL to start
sleep 5

# Set up the database and user if they don't already exist
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '$prod'\"" | grep -q 1 || su - postgres -c "psql --command \"CREATE DATABASE $prod;\""
su - postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname = 'prod'\"" | grep -q 1 || su - postgres -c "psql --command \"CREATE USER prod WITH SUPERUSER PASSWORD 'prod';\""
su - postgres -c "psql --command \"GRANT ALL PRIVILEGES ON DATABASE $prod TO prod;\""

# Run the Python application
exec "$@"
