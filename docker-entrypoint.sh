#!/bin/bash

# Start the PostgreSQL service
echo "Starting PostgreSQL service..."
service postgresql start

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL to start..."
sleep 5

# Check if the PostgreSQL service started successfully
if ! pg_isready -q; then
    echo "PostgreSQL failed to start."
    exit 1
fi

# Set up the database and user if they don't already exist
echo "Setting up the database and user..."
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = 'prod'\"" | grep -q 1 || su - postgres -c "psql --command \"CREATE DATABASE prod;\""
su - postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname = 'prod'\"" | grep -q 1 || su - postgres -c "psql --command \"CREATE USER prod WITH SUPERUSER PASSWORD 'prod';\""
su - postgres -c "psql --command \"GRANT ALL PRIVILEGES ON DATABASE prod TO prod;\""

# Check if the previous command was successful
if [ $? -ne 0 ]; then
    echo "Failed to grant privileges on database prod to user prod."
    exit 1
fi

# Run the Python application
echo "Running the Python application..."
exec "$@"
