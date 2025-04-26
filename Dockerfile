FROM python:3.9-slim

WORKDIR /app

# Install debugging tools
RUN apt-get update && apt-get install -y \
    procps \
    htop \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# List current directory for debugging
RUN ls -la

# Copy all files explicitly
COPY . .

# List contents after copying to verify files
RUN ls -la

# Make run.py executable
RUN chmod +x run.py

EXPOSE 4000

# Environment variables for debugging
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Use Python directly instead of Gunicorn
CMD ["python", "run.py"] 