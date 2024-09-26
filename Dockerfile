FROM ubuntu:latest

# Install Python, PostgreSQL, and required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    postgresql \
    libpq-dev \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Copy your Python script and requirements into the container
COPY Backend.py /app/Backend.py
COPY requirements.txt /app/requirements.txt

# Activate the virtual environment and install dependencies
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r /app/requirements.txt

# Change to the working directory
WORKDIR /app

# Expose ports for PostgreSQL and the Flask application
EXPOSE 5432 5000

# Copy the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Use the entrypoint script to initialize and run services
ENTRYPOINT ["/docker-entrypoint.sh"]

# Use the virtual environment's Python interpreter to run the app
CMD ["/opt/venv/bin/python", "/app/Backend.py"]
