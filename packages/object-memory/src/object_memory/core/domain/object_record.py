"""Modelli di dominio per gli oggetti memorizzati.

Definisce la struttura dati di un oggetto catalogato dalla pipeline:
la sua etichetta VLM, la posizione spaziale nell'inquadratura e il
record completo con la storia degli aggiornamenti.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

from vision_commons.domain.detection import BoundingBox


@dataclass(frozen=True)
class ObjectLabel:
    """Etichetta assegnata dal VLM a un oggetto rilevato.

    Attributes:
        text: Etichetta testuale (es. "maglia rossa", "bottiglia d'acqua").
        language: Codice lingua ISO 639-1 (es. "it").
        confidence: Confidenza dell'etichettatura [0, 1]. None se non
            disponibile (il VLM non sempre restituisce una confidenza).
        assigned_at: Timestamp Unix del momento di assegnazione.
    """

    text: str
    language: str = "it"
    confidence: float | None = None
    assigned_at: float = field(default_factory=time.time)


@dataclass(frozen=True)
class SpatialPosition:
    """Posizione spaziale di un oggetto in un frame.

    Esprime dove si trovava l'oggetto nell'inquadratura al momento
    dell'ultimo rilevamento. Le coordinate sono normalizzate [0, 1]
    per essere indipendenti dalla risoluzione.

    Attributes:
        bbox: Bounding box dell'oggetto nelle coordinate del frame.
        frame_width: Larghezza del frame sorgente in pixel.
        frame_height: Altezza del frame sorgente in pixel.
        timestamp: Timestamp Unix del momento del rilevamento.
    """

    bbox: BoundingBox
    frame_width: int
    frame_height: int
    timestamp: float = field(default_factory=time.time)

    @property
    def center_normalized(self) -> tuple[float, float]:
        """Centro del bbox come coordinate normalizzate (x, y) in [0, 1]."""
        cx = (self.bbox.x1 + self.bbox.x2) / 2 / self.frame_width
        cy = (self.bbox.y1 + self.bbox.y2) / 2 / self.frame_height
        return (cx, cy)

    def iou(self, other: "SpatialPosition") -> float:
        """Calcola l'Intersection over Union tra due posizioni.

        Usato da OverlapTracker per determinare se due detection
        rappresentano lo stesso oggetto fisico.

        Args:
            other: Altra posizione con cui confrontare.

        Returns:
            IoU nell'intervallo [0, 1]. 0.0 = nessuna sovrapposizione.
        """
        # TODO: implementare
        # intersection = max(0, min(self.bbox.x2, other.bbox.x2) - max(self.bbox.x1, other.bbox.x1))
        #              * max(0, min(self.bbox.y2, other.bbox.y2) - max(self.bbox.y1, other.bbox.y1))
        # union = self.bbox.area + other.bbox.area - intersection
        # return intersection / union if union > 0 else 0.0
        raise NotImplementedError


@dataclass(frozen=True)
class ObjectRecord:
    """Record completo di un oggetto memorizzato nel catalogo.

    Rappresenta un oggetto fisico distinto nell'ambiente dell'utente.
    Viene creato al primo rilevamento e aggiornato ogni volta che
    l'oggetto viene rivisto in una posizione significativamente diversa.

    Attributes:
        id: Identificatore univoco dell'oggetto (UUID).
        label: Etichetta VLM corrente dell'oggetto.
        last_position: Ultima posizione nota dell'oggetto.
        last_snapshot_path: Percorso dell'ultimo screenshot salvato.
        first_seen_at: Timestamp Unix del primo rilevamento.
        last_seen_at: Timestamp Unix dell'ultimo rilevamento.
        detection_count: Numero totale di volte che l'oggetto è stato rilevato.
    """

    id: str
    label: ObjectLabel
    last_position: SpatialPosition
    last_snapshot_path: str
    first_seen_at: float
    last_seen_at: float = field(default_factory=time.time)
    detection_count: int = 1

    @classmethod
    def create_new(
        cls,
        label: ObjectLabel,
        position: SpatialPosition,
        snapshot_path: str,
    ) -> "ObjectRecord":
        """Factory: crea un nuovo ObjectRecord per un oggetto appena rilevato.

        Args:
            label: Etichetta VLM assegnata all'oggetto.
            position: Posizione iniziale dell'oggetto.
            snapshot_path: Percorso dello screenshot iniziale.

        Returns:
            Nuovo ObjectRecord con ID UUID generato.
        """
        now = time.time()
        return cls(
            id=str(uuid.uuid4()),
            label=label,
            last_position=position,
            last_snapshot_path=snapshot_path,
            first_seen_at=now,
            last_seen_at=now,
            detection_count=1,
        )

    def with_updated_position(
        self,
        new_position: SpatialPosition,
        new_snapshot_path: str,
    ) -> "ObjectRecord":
        """Restituisce una copia aggiornata con la nuova posizione.

        Mantiene l'immutabilità: non modifica l'originale ma restituisce
        un nuovo ObjectRecord con i campi aggiornati.

        Args:
            new_position: Nuova posizione rilevata.
            new_snapshot_path: Percorso del nuovo screenshot.

        Returns:
            Nuovo ObjectRecord con posizione e snapshot aggiornati.
        """
        return ObjectRecord(
            id=self.id,
            label=self.label,
            last_position=new_position,
            last_snapshot_path=new_snapshot_path,
            first_seen_at=self.first_seen_at,
            last_seen_at=time.time(),
            detection_count=self.detection_count + 1,
        )


__all__ = ["ObjectLabel", "ObjectRecord", "SpatialPosition"]
