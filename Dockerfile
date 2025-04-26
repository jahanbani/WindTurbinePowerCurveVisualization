FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

# Make sure app.py is in the Python path
ENV PYTHONPATH=/app

# Use wsgi.py instead of directly accessing app:server
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "--log-level=debug", "wsgi:server"] 