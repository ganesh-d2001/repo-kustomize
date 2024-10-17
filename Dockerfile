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

# Copy your Python script, requirements, and static files into the container
COPY Backend.py /app/Backend.py
COPY requirements.txt /app/requirements.txt
COPY static /app/static
COPY template /app/templates

# Activate the virtual environment and install dependencies
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r /app/requirements.txt

# Create necessary directories for logs
RUN mkdir -p /app/logs

# Set the working directory
WORKDIR /app

# Expose ports for PostgreSQL and Flask
EXPOSE 5432 5000

# Copy the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set the entrypoint to initialize services
ENTRYPOINT ["/docker-entrypoint.sh"]

RUN chmod +x /app/Backend.py

# CMD to run the Flask app
CMD ["/opt/venv/bin/python", "/app/Backend.py"]
