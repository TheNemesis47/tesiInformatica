"""Tracker per l'overlap tra detection consecutive.

Determina se una nuova detection rappresenta un oggetto già noto
(stesso oggetto, stessa o simile posizione) oppure un oggetto nuovo
o spostato che richiede aggiornamento del catalogo.
"""

from __future__ import annotations

import structlog

from object_memory.core.domain.object_record import ObjectRecord, SpatialPosition
from vision_commons.domain.detection import Detection

logger = structlog.get_logger(__name__)


class OverlapTracker:
    """Tracker che confronta detection correnti con oggetti già memorizzati.

    Usa IoU (Intersection over Union) tra bounding box per determinare
    se una detection corrisponde a un oggetto già nel catalogo e se
    la sua posizione è cambiata abbastanza da giustificare un aggiornamento
    dello snapshot.

    Attributes:
        iou_threshold: IoU minimo per considerare due detection dello stesso
            oggetto. Sotto questa soglia → nuovo oggetto.
        position_update_threshold: Soglia di spostamento del centro bbox
            (normalizzato) per considerare la posizione "significativamente
            cambiata" e aggiornare lo snapshot.
    """

    def __init__(
        self,
        iou_threshold: float = 0.4,
        position_update_threshold: float = 0.15,
    ) -> None:
        """Inizializza il tracker.

        Args:
            iou_threshold: IoU minimo per matching oggetto [0, 1].
            position_update_threshold: Spostamento minimo del centro [0, 1]
                per triggherare un aggiornamento snapshot.
        """
        self.iou_threshold = iou_threshold
        self.position_update_threshold = position_update_threshold

    def find_matching_record(
        self,
        detection: Detection,
        frame_width: int,
        frame_height: int,
        known_records: list[ObjectRecord],
    ) -> ObjectRecord | None:
        """Cerca nel catalogo un oggetto che corrisponda alla detection.

        Args:
            detection: Detection corrente da confrontare.
            frame_width: Larghezza del frame corrente in pixel.
            frame_height: Altezza del frame corrente in pixel.
            known_records: Lista degli ObjectRecord già nel catalogo.

        Returns:
            Il record con IoU più alto se supera ``iou_threshold``,
            None se la detection non corrisponde a nessun oggetto noto.
        """
        # TODO: implementare
        # 1. Crea SpatialPosition dalla detection corrente
        # 2. Per ogni record in known_records:
        #    - calcola IoU tra current_position e record.last_position
        #    - tieni traccia del miglior match
        # 3. Se best_iou >= self.iou_threshold → return best_record
        # 4. return None
        raise NotImplementedError

    def should_update_snapshot(
        self,
        new_position: SpatialPosition,
        record: ObjectRecord,
    ) -> bool:
        """Determina se lo spostamento richiede un aggiornamento dello snapshot.

        Args:
            new_position: Posizione attuale rilevata.
            record: Record esistente con l'ultima posizione nota.

        Returns:
            True se il centro dell'oggetto si è spostato abbastanza da
            rendere il vecchio snapshot non più rappresentativo.
        """
        # TODO: implementare
        # 1. Calcola distanza euclidea tra new_position.center_normalized
        #    e record.last_position.center_normalized
        # 2. return distanza >= self.position_update_threshold
        raise NotImplementedError


__all__ = ["OverlapTracker"]
