"""Port per l'etichettatura VLM di un oggetto rilevato.

Implementato da GemmaObjectLabeler (adapters/labeling) che usa
GemmaVLMClient di vision-commons con prompt specifici per l'etichettatura.
"""

from __future__ import annotations

from typing import Protocol

from object_memory.core.domain.object_record import ObjectLabel
from vision_commons.domain.detection import Detection
from vision_commons.domain.frame import FrameData


class ObjectLabelerPort(Protocol):
    """Interfaccia per l'etichettatura di un oggetto tramite VLM.

    Riceve il frame e una detection, interroga il VLM per ottenere
    un'etichetta semantica dell'oggetto (es. "maglia rossa", "bottiglia").
    """

    async def label(
        self,
        frame: FrameData,
        detection: Detection,
        language: str = "it",
    ) -> ObjectLabel:
        """Assegna un'etichetta semantica all'oggetto rilevato.

        Args:
            frame: Frame originale (necessario per il contesto visivo).
            detection: Detection dell'oggetto da etichettare.
            language: Lingua dell'etichetta da generare.

        Returns:
            ObjectLabel con il testo descrittivo dell'oggetto.

        Raises:
            ObjectMemoryError: Se il VLM non risponde o l'etichettatura fallisce.
        """
        ...


__all__ = ["ObjectLabelerPort"]
