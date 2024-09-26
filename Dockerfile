FROM ubuntu:latest

# Install Python and PostgreSQL
RUN apt-get update && apt-get install -y python3 python3-pip postgresql libpq-dev flask

# Copy your Python script into the container
COPY Backend.py /app/Backend.py

# Change to the working directory
WORKDIR /app

# Install any Python dependencies
COPY requirements.txt /app/requirements.txt
#RUN pip3 install -r requirements.txt

# Expose the necessary ports
EXPOSE 5432 5000

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Use the entrypoint script to initialize and run the services
ENTRYPOINT ["/docker-entrypoint.sh"]

# CMD is used to start the python application
CMD ["python3", "/app/Backend.py"]
