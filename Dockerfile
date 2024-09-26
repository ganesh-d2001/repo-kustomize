FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
RUN apt-get install -y postgresql libpq-dev -y  
RUN su - postgres -c "psql -c 'CREATE DATABASE prod;'"
RUN su - postgres -c "psql -c 'CREATE User prod WITH PASSWORD 'prod';'"
RUN Grant all privileges on database prod to prod;
RUN python3 myscript.py
