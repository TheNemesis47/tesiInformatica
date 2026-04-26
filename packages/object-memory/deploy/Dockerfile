FROM python:3.12-slim

# Installa dipendenze sistema (OpenCV)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Installa Poetry
RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

# Copia vision-commons (path dependency)
COPY ../vision-commons/src/ /vision-commons/src/
COPY ../vision-commons/pyproject.toml /vision-commons/pyproject.toml

# Copia object-memory
COPY pyproject.toml poetry.lock* ./
COPY src/ ./src/
COPY config.yaml ./

# Installa dipendenze senza dev
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi

# Crea directory dati
RUN mkdir -p /app/data/snapshots

# Porta REST + WebSocket
EXPOSE 8766

CMD ["python", "-m", "object_memory", "--host", "0.0.0.0", "--port", "8766"]
