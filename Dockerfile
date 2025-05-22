FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the server.py is executable
RUN chmod +x server.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run when the container starts
CMD ["python", "server.py"]
