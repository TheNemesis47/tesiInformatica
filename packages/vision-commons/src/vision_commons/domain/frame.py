"""Modelli di dominio per i frame catturati dal dispositivo.

Definisce le strutture dati che rappresentano un singolo frame video
acquisito dalla sorgente (webcam Brio 4K o Meta Quest 3), comprendendo
sia i dati grezzi dell'immagine sia i metadati contestuali.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class CaptureMode(str, Enum):
    """Modalità di cattura del frame.

    Attributes:
        AUTO: Modalità automatica — la pipeline decide se descrivere
            in base al rilevamento di cambiamenti nella scena.
        POINTING: Modalità di puntamento — l'utente indica con il gesto
            un punto specifico e vuole una descrizione immediata di quell'area.
    """

    AUTO = "AUTO"
    POINTING = "POINTING"


@dataclass(frozen=True)
class FrameMetadata:
    """Metadati associati a un frame catturato.

    Attributes:
        timestamp: Timestamp Unix (secondi) del momento di acquisizione.
        mode: Modalità di cattura attiva al momento dell'acquisizione.
        pointing_coords: Coordinate normalizzate [0,1] del punto indicato
            dall'utente, presenti solo in modalità POINTING.
        crop_size: Dimensione del crop in pixel centrato su pointing_coords,
            presente solo in modalità POINTING.
        source_resolution: Risoluzione originale della sorgente (width, height)
            prima di qualsiasi pre-elaborazione.
    """

    timestamp: float = field(default_factory=time.time)
    mode: CaptureMode = CaptureMode.AUTO
    pointing_coords: tuple[float, float] | None = None
    crop_size: int | None = None
    source_resolution: tuple[int, int] = (1280, 960)


@dataclass(frozen=True)
class FrameData:
    """Frame catturato con i suoi metadati.

    Rappresenta un'immagine compressa (tipicamente JPEG) pronta per
    essere analizzata dalla pipeline. L'immutabilità garantisce che
    il frame non venga modificato durante l'elaborazione.

    Attributes:
        image_bytes: Bytes dell'immagine compressa (JPEG o PNG).
        metadata: Metadati contestuali del frame.
    """

    image_bytes: bytes
    metadata: FrameMetadata


__all__ = ["CaptureMode", "FrameData", "FrameMetadata"]
