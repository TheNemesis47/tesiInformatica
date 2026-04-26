# Meta Quest Vision — Monorepo

Monorepo delle tesi gemelle su visione artificiale assistita per Meta Quest 3.

| Pacchetto | Descrizione | Porta |
|---|---|---|
| **vision-caption** | Audio-descrizione ambientale in tempo reale | 8765 |
| **object-memory** | Catalogo visivo degli oggetti con ricerca vocale | 8766 |
| **vision-commons** | Libreria condivisa (frame, detection, VLM, SSIM) | — |

---

## Architettura

Entrambi i progetti seguono la **Hexagonal Architecture** (Ports & Adapters):

```
┌──────────────────────────────────────────────────────────┐
│  infrastructure (FastAPI, config, DI container)          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  adapters (OpenCV, RF-DETR, Ollama, Chatterbox...) │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │  core (domain models, ports, services)       │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
        ↑ importa da
┌──────────────────────┐
│   vision-commons     │  FrameData, Detection, SSIM,
│   (lib condivisa)    │  GemmaVLMClient, FrameSource…
└──────────────────────┘
```

**Regola fondamentale**: `core/` non importa MAI librerie esterne.

---

## Struttura

```
meta-quest-vision-monorepo/
├── packages/
│   ├── vision-commons/          # Libreria condivisa
│   │   └── src/vision_commons/
│   │       ├── domain/          # FrameData, BoundingBox, Detection, SceneAnalysis
│   │       ├── ports/           # FrameSourcePort, SceneDetectorPort, FramePreprocessorPort
│   │       ├── adapters/        # WebcamSource, SSIMDetector, RFDETRDetector, GemmaVLMClient
│   │       ├── infrastructure/  # Logging (structlog), LatencyTracker
│   │       └── shared/          # Type aliases (ImageBytes, LanguageCode, Milliseconds)
│   │
│   ├── vision-caption/          # Tesi: audio-descrizione ambientale
│   │   ├── src/vision_caption/
│   │   │   ├── core/            # Caption, AudioResult, CaptionGeneratorPort, CaptionPipeline
│   │   │   ├── adapters/        # GemmaCaptionGenerator, ChatterboxSynthesizer, OpusEncoder
│   │   │   └── infrastructure/  # FastAPI server, container DI, AppSettings
│   │   ├── tests/
│   │   ├── scripts/             # test_client_webcam.py, benchmark_latency.py…
│   │   ├── deploy/              # Dockerfile, docker-compose, slurm_job.sh
│   │   └── config.yaml
│   │
│   └── object-memory/           # Tesi collega: catalogo visivo oggetti
│       ├── src/object_memory/
│       │   ├── core/            # ObjectRecord, SnapshotQuery, OverlapTracker, QueryService
│       │   ├── adapters/        # GemmaObjectLabeler, SQLiteRepository, FileSystemSnapshotStore
│       │   └── infrastructure/  # FastAPI server, container DI, AppSettings
│       ├── tests/
│       ├── scripts/             # test_client.py, benchmark_query.py…
│       ├── deploy/              # Dockerfile, docker-compose, slurm_job.sh
│       └── config.yaml
│
├── .ruff.toml                   # Config ruff condivisa
├── .pre-commit-config.yaml      # Hook pre-commit condivisi
└── pyproject.toml               # Root (solo dev tools)
```

---

## Requisiti

- **Python 3.12**
- **uv** — `curl -LsSf https://astral.sh/uv/install.sh | sh` (oppure `brew install uv`)
- **GPU NVIDIA** con CUDA 12.x
- **Ollama** con modello `gemma4:e4b`
- Webcam o Meta Quest 3

---

## Installazione

Il monorepo usa **uv workspace**: un solo `uv sync --all-packages` dalla root installa tutti i pacchetti in modalità editable, con un unico `.venv` e un unico lock file (`uv.lock`).

```bash
# dalla root del monorepo
uv sync --all-packages
```

Il flag `--all-packages` è necessario perché di default `uv sync` installa solo il root del workspace; con `--all-packages` installa anche tutti i membri (`vision-commons`, `vision-caption`, `object-memory`).

Questo crea `.venv/` alla root con `vision-commons`, `vision-caption` e `object-memory` tutti installati in editable. Modificare un file `.py` in qualunque package è immediato — niente reinstallazione.

---

## Avvio

Tutti i comandi vanno lanciati dalla **root** del monorepo.

### vision-caption

```bash
ollama pull gemma4:e4b

uv run --package vision-caption python -m vision_caption     # server su :8765
# oppure
uv run --package vision-caption vision-caption

# Client di test con webcam
uv run --package vision-caption python packages/vision-caption/scripts/test_client_webcam.py --host localhost --port 8765
```

### object-memory

```bash
uv run --package object-memory python -m object_memory       # server su :8766
# oppure
uv run --package object-memory object-memory

# Client di test
uv run --package object-memory python packages/object-memory/scripts/test_client.py --host localhost --port 8766

# Query
uv run --package object-memory python packages/object-memory/scripts/query_objects.py --query "maglia rossa"
```

---

## Test

```bash
# vision-caption
uv run --package vision-caption pytest packages/vision-caption/tests/unit/
uv run --package vision-caption pytest packages/vision-caption/tests/integration/ -v

# object-memory
uv run --package object-memory pytest packages/object-memory/tests/unit/

# vision-commons
uv run --package vision-commons pytest packages/vision-commons/tests/
```

---

## Deploy

Ogni pacchetto ha la sua directory `deploy/` con:
- `Dockerfile` — immagine standalone
- `docker-compose.yml` — stack completo con Ollama
- `slurm_job.sh` — job per cluster PurpleJeans HPC

```bash
# vision-caption
cd packages/vision-caption
docker compose -f deploy/docker-compose.yml up

# object-memory
cd packages/object-memory
docker compose -f deploy/docker-compose.yml up
```

---

## Pipeline di elaborazione

### vision-caption

```
Frame (JPEG) → WebSocket
    ↓
[Scene Detection]  SSIM → RF-DETR
    ↓ scene_changed=True
[Rate Limiter]
    ↓
[VLM Caption]  Gemma 4 via Ollama
    ↓
[TTS Synthesis]  Chatterbox Turbo
    ↓
Audio (WAV/Opus) → WebSocket → Client
```

### object-memory

```
Frame (JPEG) → WebSocket
    ↓
[Scene Detection]  SSIM (skip se invariato)
    ↓
[Object Detection]  RF-DETR → lista Detection
    ↓ per ogni Detection
[IoU Matching]  cerca record esistente (OverlapTracker)
    ├─ match → aggiorna posizione / snapshot se necessario
    └─ no match → crea nuovo ObjectRecord + label VLM
    ↓
[Persist]  SQLite + filesystem snapshot
    ↓
ACK {"type": "ack", "updated": N} → WebSocket

Query REST:
GET  /api/objects         → lista tutti gli oggetti
POST /api/query           → cerca per etichetta testuale
GET  /api/objects/{id}/snapshot → screenshot base64
```
