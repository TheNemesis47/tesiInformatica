"""Modelli di dominio per il rilevamento di oggetti e l'analisi della scena.

Definisce le strutture dati prodotte dal componente di scene detection:
bounding box, detection di singoli oggetti e l'analisi complessiva della scena
che determina se è necessario generare una nuova caption.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass(frozen=True)
class BoundingBox:
    """Bounding box di un oggetto rilevato, in coordinate pixel assolute.

    Attributes:
        x1: Coordinata X del bordo sinistro.
        y1: Coordinata Y del bordo superiore.
        x2: Coordinata X del bordo destro.
        y2: Coordinata Y del bordo inferiore.
    """

    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        """Larghezza del bounding box in pixel."""
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        """Altezza del bounding box in pixel."""
        return self.y2 - self.y1

    @property
    def area(self) -> float:
        """Area del bounding box in pixel quadrati."""
        return self.width * self.height

    @property
    def center(self) -> tuple[float, float]:
        """Centro del bounding box come (x, y)."""
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


@dataclass(frozen=True)
class Detection:
    """Singolo oggetto rilevato in un frame.

    Attributes:
        class_name: Nome della classe dell'oggetto (es. "person", "chair").
        confidence: Score di confidenza del modello nell'intervallo [0, 1].
        bbox: Bounding box dell'oggetto nell'immagine.
    """

    class_name: str
    confidence: float
    bbox: BoundingBox


@dataclass(frozen=True)
class SceneAnalysis:
    """Risultato dell'analisi di una scena da parte dello SceneDetector.

    Aggrega il risultato di uno o più detector (SSIM, RF-DETR) per determinare
    se la scena è cambiata in modo significativo rispetto al frame precedente.

    Attributes:
        detections: Tuple di oggetti rilevati nel frame corrente.
        scene_changed: True se la scena è cambiata abbastanza da giustificare
            una nuova caption.
        ssim_score: Score SSIM rispetto al frame precedente (1.0 = identico,
            0.0 = completamente diverso). None se SSIM non è stato calcolato.
        semantic_diff: Differenza semantica stimata basata sulle detection
            (0.0 = nessuna differenza, 1.0 = differenza massima). None se
            RF-DETR non è stato usato.
        timestamp: Timestamp Unix del momento dell'analisi.
    """

    detections: tuple[Detection, ...]
    scene_changed: bool
    ssim_score: float | None = None
    semantic_diff: float | None = None
    timestamp: float = field(default_factory=time.time)


__all__ = ["BoundingBox", "Detection", "SceneAnalysis"]
