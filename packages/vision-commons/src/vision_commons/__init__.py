"""vision-commons — componenti condivisi tra vision-caption e object-memory.

Fornisce le astrazioni e le implementazioni concrete riusabili:
- Modelli di dominio condivisi (FrameData, Detection, SceneAnalysis)
- Port condivisi (FrameSourcePort, SceneDetectorPort, FramePreprocessorPort)
- Adapter concreti (SSIM, RF-DETR, OpenCV, frame sources)
- Client VLM di basso livello (GemmaVLMClient)
- Infrastruttura trasversale (logging, latency tracker)
"""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
