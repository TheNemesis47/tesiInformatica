"""Port per il rilevamento di oggetti nel frame.

Implementato da RFDETRSceneDetector (vision-commons) che però restituisce
SceneAnalysis. Questo port è un alias semantico più specifico per object-memory:
vuole esplicitamente le detection, non solo il flag scene_changed.
"""

from __future__ import annotations

from typing import Protocol

from vision_commons.domain.detection import Detection
from vision_commons.domain.frame import FrameData


class ObjectDetectorPort(Protocol):
    """Interfaccia per il rilevamento di oggetti in un frame.

    Differisce da SceneDetectorPort (commons) perché l'obiettivo qui
    non è rilevare se la scena è cambiata, ma estrarre tutti gli oggetti
    presenti nel frame con le loro bounding box.
    """

    def detect(self, frame: FrameData) -> tuple[Detection, ...]:
        """Rileva tutti gli oggetti presenti nel frame.

        Args:
            frame: Frame da analizzare.

        Returns:
            Tuple di Detection con classe, confidenza e bounding box
            per ogni oggetto rilevato sopra la soglia di confidenza.
        """
        ...


__all__ = ["ObjectDetectorPort"]
