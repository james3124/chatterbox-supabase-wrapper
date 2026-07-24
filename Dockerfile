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
    pip install --no-cache-dir cython numpy && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 torchaudio==2.6.0 && \
    pip install --no-cache-dir --no-build-isolation chatterbox-tts==0.1.7 && \
    python3 -c "import chatterbox; print('chatterbox path:', chatterbox.__file__); from chatterbox.tts_turbo import ChatterboxTurboTTS; print('chatterbox-tts OK')" && \
    pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Copy the application
COPY . .

# Expose the FastAPI port
EXPOSE 10000

# Start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]