# Dockerfile
FROM python:3.9

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy project
COPY . .

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Run the application
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 run:app"]