FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
RUN apt-get install -y postgresql libpq-dev -y  
USER postgres

# Set environment variables
ENV POSTGRES_USER =postgres
ENV POSTGRES_PASSWORD=your_password
ENV POSTGRES_DB=prod
RUN service postgresql start && \
    psql --command "CREATE USER prod WITH SUPERUSER PASSWORD 'prod';" && \
    psql --command "CREATE DATABASE prod;" && \
    psql --command "ALTER USER prod WITH PASSWORD 'prod';" &&\
    psql --command "Grant all privileges on database prod to prod;"
USER root

# Copy your Python script into the container
COPY Backend.py /app/Backend.py
        
# Change to the working directory
WORKDIR /app
        
# Install any Python dependencies (if you have a requirements.txt)
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5432
EXPOSE 5000

