# Dockerfile for Agriculture Advisory System

FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies for voice processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    ffmpeg \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Handle PyAudio installation
RUN pip install --no-cache-dir pyaudio || \
    (apt-get update && apt-get install -y python3-pyaudio && rm -rf /var/lib/apt/lists/*)

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p models datasets uploads static/css static/js static/images templates logs instance

# Set permissions
RUN chmod -R 755 . && \
    chmod -R 777 uploads && \
    chmod -R 777 instance && \
    chmod -R 777 logs

# Initialize database and train models
RUN python -c "from app import app, db; app.app_context().push(); db.create_all()" && \
    python train_models.py || echo "Model training skipped" && \
    python -c "from app import app; from populate_database import populate_sample_data; app.app_context().push(); populate_sample_data()" || echo "Data population skipped"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "app:app"]