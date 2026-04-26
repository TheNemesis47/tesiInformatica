# vision-caption

Server WebSocket per **audio-descrizione ambientale in tempo reale** per utenti ciechi/ipovedenti. Riceve frame da Meta Quest 3 (o webcam Brio in dev), rileva cambi di scena, genera una caption con Gemma 4, sintetizza voce con Chatterbox e rispedisce audio al client.

Porta di default: **8765**.

## Pipeline

```
Frame JPEG (WebSocket in)
    ↓
SSIM scene change?  ──no──→ scarta
    ↓ sì
Rate limiter (min_interval_sec)  ──blocca──→ scarta
    ↓ ok
Gemma 4 (VLM) → caption testuale italiana
    ↓
Chatterbox TTS → audio WAV/Opus
    ↓
WebSocket out → client
```

## Struttura

```
src/vision_caption/
├── core/                    # PURO. nessuna libreria esterna.
│   ├── domain/
│   │   ├── caption.py       # Caption, CaptionRequest
│   │   └── audio.py         # AudioResult
│   ├── ports/               # interfacce specifiche di questo progetto
│   │   ├── caption_generator.py   # CaptionGeneratorPort
│   │   ├── speech_synthesizer.py  # SpeechSynthesizerPort
│   │   └── audio_encoder.py       # AudioEncoderPort
│   ├── services/
│   │   ├── caption_pipeline.py    # CaptionPipeline — orchestratore
│   │   └── rate_limiter.py        # RateLimiter (già implementato)
│   └── events.py            # eventi di dominio (CaptionGeneratedEvent...)
│
├── adapters/                # implementazioni concrete
│   ├── captioning/
│   │   ├── gemma_caption.py # adapter sopra GemmaVLMClient (di vision-commons)
│   │   ├── mock_caption.py  # mock per test (già funzionante)
│   │   └── prompts/         # template italiani per i prompt VLM
│   ├── speech/
│   │   ├── chatterbox_synth.py # TTS reale (richiede GPU)
│   │   └── mock_synth.py       # mock con WAV silenzioso
│   └── audio_encoding/
│       └── opus_encoder.py
│
├── infrastructure/
│   ├── config/
│   │   └── settings.py      # AppSettings (Pydantic, legge config.yaml + env)
│   ├── server/
│   │   ├── app.py           # factory FastAPI
│   │   ├── websocket_handler.py # handler WS principale
│   │   ├── health.py        # endpoint /health
│   │   └── middleware.py    # logging, latency
│   └── container.py         # Composition Root — costruisce la pipeline
│
├── shared/
│   └── errors.py            # CaptionGenerationError, SpeechSynthesisError
│
└── __main__.py              # `python -m vision_caption`
```

## Cosa importa da vision-commons

- `FrameData`, `CaptureMode`, `FrameMetadata` (domain)
- `Detection`, `SceneAnalysis` (domain)
- `SceneDetectorPort` (port)
- `SSIMDetector`, `HybridDetector` (adapter scene)
- `WebcamSource`, `StaticImageSource` (adapter frame)
- `GemmaVLMClient` (adapter VLM)
- `LatencyTracker` (infrastructure)

## Stato implementazione

| Componente | Stato |
|---|---|
| `RateLimiter` | implementato |
| `CaptionPipeline.process()` | TODO numerati, `raise NotImplementedError` |
| `GemmaCaptionGenerator` | TODO, da collegare a `GemmaVLMClient` di vision-commons |
| `ChatterboxSynthesizer` | TODO, richiede GPU NVIDIA |
| `OpusEncoder` | TODO |
| `MockCaptionGenerator`, `MockSynthesizer` | implementati |
| WebSocket handler | scheletro |
| FastAPI app + DI container | scheletro |

## Avvio rapido

Prerequisito: dalla **root** del monorepo aver eseguito `uv sync` almeno una volta (vedi README root). Poi:

```bash
ollama pull gemma4:e4b

# dalla root del monorepo
uv run --package vision-caption python -m vision_caption     # server su :8765

# in alternativa, usando lo script registrato in [project.scripts]
uv run --package vision-caption vision-caption
```

Test client (altra shell):
```bash
uv run --package vision-caption python packages/vision-caption/scripts/test_client_webcam.py --host localhost --port 8765
```

Test:
```bash
uv run --package vision-caption pytest packages/vision-caption/tests/unit/
uv run --package vision-caption pytest packages/vision-caption/tests/integration/ -v
```
