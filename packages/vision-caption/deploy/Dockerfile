FROM python:3.12-slim

# Installa dipendenze sistema (OpenCV, audio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Installa Poetry
RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

# Copia vision-commons (path dependency)
COPY ../vision-commons/pyproject.toml ../vision-commons/src/ /vision-commons/src/
COPY ../vision-commons/pyproject.toml /vision-commons/pyproject.toml

# Copia vision-caption
COPY pyproject.toml poetry.lock* ./
COPY src/ ./src/
COPY config.yaml ./

# Installa dipendenze senza dev
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

# Porta WebSocket
EXPOSE 8765

CMD ["python", "-m", "vision_caption", "--host", "0.0.0.0", "--port", "8765"]
