FROM ubuntu:latest

# Install Python, PostgreSQL, and required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Activate the virtual environment and install dependencies
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose ports for PostgreSQL and Flask
EXPOSE 5000

# Set the entrypoint to initialize services
RUN chmod +x /app/Backend.py

# CMD to run the Flask app
CMD ["/opt/venv/bin/python", "/app/Backend.py"]
