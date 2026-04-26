"""Modelli di dominio per le caption testuali generate dal VLM.

Definisce la richiesta di caption (input al CaptionGenerator) e la caption
prodotta (output), includendo metadati di latenza utili per il benchmark
della tesi.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from vision_commons.domain.frame import CaptureMode, FrameData


@dataclass(frozen=True)
class CaptionRequest:
    """Richiesta di generazione caption da inviare al VLM.

    Attributes:
        frame: Frame da descrivere.
        mode: Modalità di cattura che determina il prompt da usare.
        prompt_override: Prompt personalizzato che sovrascrive il template
            predefinito per la modalità. None per usare il default.
    """

    frame: FrameData
    mode: CaptureMode
    prompt_override: str | None = None


@dataclass(frozen=True)
class Caption:
    """Caption testuale generata dal VLM per un frame.

    Attributes:
        text: Testo della descrizione generata.
        mode: Modalità di cattura usata per la generazione.
        language: Codice lingua ISO 639-1 della caption (es. "it", "en").
        generation_time_ms: Tempo impiegato per generare la caption in
            millisecondi. Usato per il benchmark della tesi.
        timestamp: Timestamp Unix del momento di completamento della
            generazione.
    """

    text: str
    mode: CaptureMode
    language: str = "it"
    generation_time_ms: float = 0.0
    timestamp: float = field(default_factory=time.time)


__all__ = ["Caption", "CaptionRequest"]
