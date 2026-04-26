"""Mock labeler per test senza GPU."""

from __future__ import annotations

import time

from object_memory.core.domain.object_record import ObjectLabel
from vision_commons.domain.detection import Detection
from vision_commons.domain.frame import FrameData

_MOCK_LABELS: dict[str, str] = {
    "person": "persona in piedi",
    "chair": "sedia grigia",
    "bottle": "bottiglia acqua",
    "cup": "tazza bianca",
    "book": "libro",
    "laptop": "laptop argento",
    "cell phone": "telefono nero",
    "bag": "borsa",
}


class MockObjectLabeler:
    """Labeler mock per test senza GPU.

    Restituisce etichette predefinite basate sul class_name della detection.
    Mantiene un contatore delle chiamate.

    Attributes:
        call_count: Numero di chiamate a ``label()`` dall'istanziazione.
    """

    def __init__(self) -> None:
        """Inizializza il mock labeler."""
        self.call_count: int = 0

    async def label(
        self,
        frame: FrameData,
        detection: Detection,
        language: str = "it",
    ) -> ObjectLabel:
        """Restituisce un'etichetta mock basata sul class_name della detection.

        Args:
            frame: Frame (ignorato nel mock).
            detection: Detection con il class_name da mappare.
            language: Lingua (ignorata nel mock).

        Returns:
            ObjectLabel con etichetta predefinita.
        """
        self.call_count += 1
        text = _MOCK_LABELS.get(detection.class_name, f"oggetto {detection.class_name}")
        return ObjectLabel(text=text, language=language)


__all__ = ["MockObjectLabeler"]
