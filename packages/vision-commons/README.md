# vision-commons

Libreria condivisa tra **vision-caption** e **object-memory**. Non è un'applicazione: non si avvia, non ha entrypoint, non ha un server. Espone domini, port e adapter riusabili.

## Cosa contiene

```
src/vision_commons/
├── domain/              # modelli dati (immutabili, senza dipendenze)
│   ├── frame.py         # FrameData, FrameMetadata, CaptureMode (AUTO/POINTING)
│   └── detection.py     # Detection, BoundingBox, SceneAnalysis
│
├── ports/               # interfacce astratte (Protocol)
│   ├── frame_source.py        # FrameSourcePort       — sorgenti video
│   ├── scene_detector.py      # SceneDetectorPort     — rileva scene change
│   └── frame_preprocessor.py  # FramePreprocessorPort — resize/normalizzazione
│
├── adapters/            # implementazioni concrete (toccano librerie esterne)
│   ├── frame_source/       # WebcamSource, VideoFileSource, StaticImageSource
│   ├── scene_detection/    # SSIMDetector, RFDETRDetector, HybridDetector
│   ├── preprocessing/      # OpenCVPreprocessor
│   └── vlm/                # GemmaVLMClient (client Ollama riusato dai due progetti)
│
├── infrastructure/
│   ├── logging/         # setup structlog condiviso
│   └── metrics/         # LatencyTracker per benchmark tesi
│
└── shared/              # type alias (ImageBytes, Milliseconds, LanguageCode)
```

## Quando importare da qui

| Cosa ti serve | Importa da |
|---|---|
| Tipo di un frame video | `vision_commons.domain.frame` |
| Bounding box / detection RF-DETR | `vision_commons.domain.detection` |
| Acquisire frame da webcam | `vision_commons.adapters.frame_source.webcam_source` |
| Rilevare cambio scena (SSIM) | `vision_commons.adapters.scene_detection.ssim_detector` |
| Chiamare Gemma 4 via Ollama | `vision_commons.adapters.vlm.gemma_client` |
| Misurare latenza per la tesi | `vision_commons.infrastructure.metrics.latency` |

## Dipendenze esterne

Pesanti (sono qui perché entrambi i progetti le usano):
`rfdetr`, `scikit-image`, `opencv-python-headless`, `ollama`, `torch`, `structlog`, `pydantic`.

## Regola architetturale

- `domain/` e `ports/` non importano nulla di esterno (solo stdlib + pydantic).
- `adapters/` possono usare librerie AI/ML, ma devono implementare un Protocol di `ports/`.
- Né `vision-caption` né `object-memory` devono avere copie locali di ciò che è qui — se serve a entrambi, si promuove a vision-commons.

## Stato implementazione

Scaffolding completo. Tutti gli adapter hanno firma + docstring + `raise NotImplementedError` con TODO numerati nel corpo. Da implementare in ordine consigliato:

1. `SSIMSceneDetector.analyze()`
2. `RFDETRDetector.detect()`
3. `GemmaVLMClient.generate()`
4. `WebcamSource.frames()`
5. `OpenCVPreprocessor.preprocess()`

## Test

```bash
# dalla root del monorepo (dopo uv sync)
uv run --package vision-commons pytest packages/vision-commons/tests/
```
