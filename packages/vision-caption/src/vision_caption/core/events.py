"""Eventi di dominio della pipeline vision-caption.

Gli eventi rappresentano fatti accaduti nel sistema. Possono essere usati
per disaccoppiare i componenti, per logging strutturato e per metriche
di latenza end-to-end.

Tutti gli eventi sono dataclass immutabili con un timestamp di creazione.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from vision_caption.core.domain.audio import AudioResult
from vision_caption.core.domain.caption import Caption
from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData


@dataclass(frozen=True)
class SceneChangedEvent:
    """Emesso quando lo SceneDetector rileva un cambiamento significativo.

    Attributes:
        frame: Frame che ha causato il rilevamento del cambiamento.
        analysis: Risultato completo dell'analisi della scena.
        timestamp: Timestamp Unix del momento di rilevamento.
    """

    frame: FrameData
    analysis: SceneAnalysis
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class CaptionGeneratedEvent:
    """Emesso quando il VLM ha generato con successo una caption.

    Attributes:
        caption: Caption testuale generata.
        frame: Frame sorgente che ha originato la caption.
        timestamp: Timestamp Unix del momento di completamento.
    """

    caption: Caption
    frame: FrameData
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class AudioSynthesizedEvent:
    """Emesso quando il TTS ha sintetizzato l'audio per una caption.

    Attributes:
        audio: Risultato audio pronto per l'invio al client.
        caption: Caption testuale da cui è stato generato l'audio.
        timestamp: Timestamp Unix del momento di completamento.
    """

    audio: AudioResult
    caption: Caption
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class PipelineErrorEvent:
    """Emesso quando si verifica un errore non recuperabile nella pipeline.

    Attributes:
        error: Eccezione che ha causato l'errore.
        stage: Stadio della pipeline in cui si è verificato l'errore
            (es. "scene_detection", "captioning", "synthesis").
        frame: Frame che stava venendo processato al momento dell'errore.
            None se l'errore è avvenuto prima dell'acquisizione del frame.
        timestamp: Timestamp Unix del momento dell'errore.
    """

    error: Exception
    stage: str
    frame: FrameData | None
    timestamp: float = field(default_factory=time.time)


__all__ = [
    "AudioSynthesizedEvent",
    "CaptionGeneratedEvent",
    "PipelineErrorEvent",
    "SceneChangedEvent",
]
