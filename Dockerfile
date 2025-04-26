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
RUN echo "Initial directory contents:" && ls -la

# Copy all files explicitly
COPY . .

# List contents after copying to verify files
RUN echo "After copying, directory contents:" && ls -la /app

# Make run.py executable
RUN chmod +x /app/run.py

EXPOSE 4000

# Environment variables for debugging
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Debug command to show files before running
CMD echo "Final directory contents:" && ls -la /app && python /app/run.py 