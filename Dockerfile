FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        git \
        build-essential \
        python3-dev \
        libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose the FastAPI port
EXPOSE 10000

# Start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]