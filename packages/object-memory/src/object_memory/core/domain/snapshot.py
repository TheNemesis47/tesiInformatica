"""Modelli di dominio per gli snapshot degli oggetti e le query.

Definisce i modelli usati per recuperare informazioni su un oggetto
memorizzato in risposta alla domanda dell'utente.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from object_memory.core.domain.object_record import ObjectRecord, SpatialPosition


@dataclass(frozen=True)
class ObjectSnapshot:
    """Snapshot completo di un oggetto per la risposta all'utente.

    Aggrega tutte le informazioni necessarie per rispondere a
    "dove si trova X?": il record dell'oggetto, il percorso dell'immagine
    e metadati per il rendering sul Meta Quest 3.

    Attributes:
        record: Record completo dell'oggetto.
        snapshot_bytes: Bytes dello screenshot (JPEG) dell'ultima posizione.
        response_text: Testo da sintetizzare vocalmente (es. "La maglia rossa
            è stata vista 5 minuti fa sul lato sinistro dell'inquadratura.").
        query_timestamp: Timestamp Unix del momento della query.
    """

    record: ObjectRecord
    snapshot_bytes: bytes
    response_text: str
    query_timestamp: float = field(default_factory=time.time)


@dataclass(frozen=True)
class SnapshotQuery:
    """Query dell'utente per trovare un oggetto.

    Attributes:
        query_text: Testo della query (es. "maglia rossa", "bottiglia").
        language: Lingua della query (codice ISO 639-1).
        max_results: Numero massimo di risultati da restituire.
        max_age_sec: Età massima (secondi) degli snapshot da considerare.
            None = nessun limite di età.
    """

    query_text: str
    language: str = "it"
    max_results: int = 3
    max_age_sec: float | None = None


__all__ = ["ObjectSnapshot", "SnapshotQuery"]
