FROM ubuntu:latest

# Install Python, PostgreSQL client libraries, and required dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate virtual environment by default
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies (including packaging for LooseVersion replacement)
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application into the container
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

# CMD to run the Flask app
CMD ["python", "/app/Backend.py"]
