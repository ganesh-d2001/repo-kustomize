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
RUN su - postgres -c "psql -c 'CREATE User prod WITH PASSWORD 'prod';'"
RUN su - postgres -c "psql -c 'CREATE DATABASE prod;'"
RUN Grant all privileges on database prod to prod;
RUN python3 myscript.py

EXPOSE 5432

