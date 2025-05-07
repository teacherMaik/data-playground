FROM python:3.10-slim

# Install dependencies for Berkeley DB and Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libdb-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your local code into the container
COPY berkeley_to_sqlight.py .
COPY traffic_berk.db .

# Install Python package that wraps Berkeley DB
RUN pip install berkeleydb

# Default command (you can change this)
CMD ["python", "berkeley_to_sqlight.py"]
