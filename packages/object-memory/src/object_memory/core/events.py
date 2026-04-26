"""Eventi di dominio di object-memory."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from object_memory.core.domain.object_record import ObjectRecord
from vision_commons.domain.frame import FrameData


@dataclass(frozen=True)
class ObjectDetectedEvent:
    """Emesso quando RF-DETR rileva nuovi oggetti in un frame.

    Attributes:
        frame: Frame che ha originato le detection.
        detection_count: Numero di oggetti rilevati.
        timestamp: Timestamp Unix del rilevamento.
    """

    frame: FrameData
    detection_count: int
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class ObjectCatalogedEvent:
    """Emesso quando un nuovo oggetto viene aggiunto al catalogo.

    Attributes:
        record: Record del nuovo oggetto salvato nel DB.
        timestamp: Timestamp Unix dell'aggiunta.
    """

    record: ObjectRecord
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class ObjectUpdatedEvent:
    """Emesso quando la posizione di un oggetto esistente viene aggiornata.

    Attributes:
        record: Record aggiornato dell'oggetto.
        previous_snapshot_path: Percorso dello snapshot precedente (ora sostituito).
        timestamp: Timestamp Unix dell'aggiornamento.
    """

    record: ObjectRecord
    previous_snapshot_path: str
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class ObjectQueryEvent:
    """Emesso quando l'utente effettua una query di ricerca.

    Attributes:
        query_text: Testo della query dell'utente.
        results_count: Numero di risultati trovati.
        timestamp: Timestamp Unix della query.
    """

    query_text: str
    results_count: int
    timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class PipelineErrorEvent:
    """Emesso quando si verifica un errore nella pipeline.

    Attributes:
        error: Eccezione che ha causato l'errore.
        stage: Stadio della pipeline dove si è verificato l'errore.
        frame: Frame processato al momento dell'errore. None se non disponibile.
        timestamp: Timestamp Unix dell'errore.
    """

    error: Exception
    stage: str
    frame: FrameData | None
    timestamp: float = field(default_factory=time.time)


__all__ = [
    "ObjectCatalogedEvent",
    "ObjectDetectedEvent",
    "ObjectQueryEvent",
    "ObjectUpdatedEvent",
    "PipelineErrorEvent",
]
