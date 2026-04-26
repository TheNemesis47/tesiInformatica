# object-memory

Server per la **memoria visiva degli oggetti**: cataloga ciò che la persona vede tramite Meta Quest 3 e permette di ritrovarlo via query testuale o vocale ("dove ho lasciato la maglia rossa?"). Tesi gemella di vision-caption.

Porta di default: **8766**.

## Pipeline

```
Frame JPEG (WebSocket in)
    ↓
SSIM: scena cambiata?  ──no──→ ack 0
    ↓ sì
RF-DETR → lista Detection (bbox + classe + score)
    ↓ per ogni detection
OverlapTracker (IoU) → matcha con record già noti
    ├── nuovo oggetto → Gemma label semantico → salva snapshot + DB
    ├── oggetto noto, spostato → aggiorna snapshot + posizione
    └── oggetto noto, fermo → nessuna azione
    ↓
SQLite (record) + filesystem (screenshot)
    ↓
ack {"updated": N} → client

REST (separato dal WS):
GET  /api/objects                     → lista oggetti
POST /api/query  { "query": "..." }  → ricerca per etichetta
GET  /api/objects/{id}/snapshot       → screenshot base64
```

## Struttura

```
src/object_memory/
├── core/                    # PURO
│   ├── domain/
│   │   ├── object_record.py # ObjectRecord, ObjectLabel, SpatialPosition
│   │   └── snapshot.py      # SnapshotQuery
│   ├── ports/
│   │   ├── object_detector.py    # ObjectDetectorPort (RF-DETR)
│   │   ├── object_labeler.py     # ObjectLabelerPort (VLM)
│   │   ├── object_repository.py  # ObjectRepositoryPort (DB)
│   │   └── snapshot_store.py     # SnapshotStorePort (filesystem)
│   ├── services/
│   │   ├── memory_pipeline.py    # ObjectMemoryPipeline — orchestratore
│   │   ├── overlap_tracker.py    # IoU matching detection↔record
│   │   └── query_service.py      # ricerca semantica per etichetta
│   └── events.py
│
├── adapters/
│   ├── labeling/
│   │   ├── gemma_labeler.py      # adapter su GemmaVLMClient di vision-commons
│   │   ├── mock_labeler.py
│   │   └── prompts/              # template per estrarre etichette da bbox
│   ├── repository/
│   │   ├── sqlite_repository.py  # aiosqlite
│   │   └── mock_repository.py
│   └── snapshot_store/
│       ├── filesystem_store.py   # PNG/JPEG su disco
│       └── mock_store.py
│
├── infrastructure/
│   ├── config/settings.py
│   ├── server/
│   │   ├── app.py
│   │   ├── websocket_handler.py  # ingest frame
│   │   ├── query_handler.py      # endpoint REST query
│   │   └── health.py
│   └── container.py
│
└── shared/errors.py
```

## Cosa importa da vision-commons

- `FrameData`, `Detection`, `BoundingBox`, `SceneAnalysis`
- `SceneDetectorPort` (riusa lo stesso SSIM detector di vision-caption)
- `RFDETRDetector` (object detection)
- `GemmaVLMClient` (per etichettare oggetti)
- `LatencyTracker`

## Stato implementazione

| Componente | Stato |
|---|---|
| `ObjectMemoryPipeline.process()` | TODO numerati, `raise NotImplementedError` |
| `OverlapTracker` (IoU matching) | TODO — è il cuore del progetto |
| `GemmaObjectLabeler` | TODO |
| `SQLiteRepository` (aiosqlite) | TODO |
| `FilesystemSnapshotStore` | TODO |
| `MockRepository`, `MockSnapshotStore` | implementati |
| WebSocket handler | scheletro |
| REST `/api/objects`, `/api/query` | scheletro |

## Avvio rapido

Prerequisito: dalla **root** del monorepo aver eseguito `uv sync` almeno una volta (vedi README root). Poi:

```bash
# dalla root del monorepo
uv run --package object-memory python -m object_memory     # server su :8766

# in alternativa
uv run --package object-memory object-memory
```

Test client:
```bash
uv run --package object-memory python packages/object-memory/scripts/test_client.py --host localhost --port 8766
uv run --package object-memory python packages/object-memory/scripts/query_objects.py --query "maglia rossa"
```

Test:
```bash
uv run --package object-memory pytest packages/object-memory/tests/unit/
```
