FROM ubuntu:latest

# Install Python and PostgreSQL
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql \
    libpq-dev

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=prod

# Start PostgreSQL service and set up the database
RUN service postgresql start && \
    psql --command "CREATE USER prod WITH SUPERUSER PASSWORD 'prod';" && \
    psql --command "CREATE DATABASE prod;" && \
    psql --command "ALTER USER prod WITH PASSWORD 'prod';" && \
    psql --command "GRANT ALL PRIVILEGES ON DATABASE prod TO prod;"

# Copy your Python script into the container
COPY Backend.py /app/Backend.py

# Change to the working directory
WORKDIR /app

# Install any Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Expose the necessary ports
EXPOSE 5432 5000

# Start PostgreSQL and your Python app
CMD service postgresql start && python3 Backend.py
