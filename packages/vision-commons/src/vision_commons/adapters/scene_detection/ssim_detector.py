"""Adapter per il rilevamento di cambiamenti di scena tramite SSIM.

Usa l'indice di similarità strutturale (Structural Similarity Index Measure)
di scikit-image per confrontare il frame corrente con il precedente.
SSIM è veloce e sensibile a cambiamenti di illuminazione e movimento.
"""

from __future__ import annotations

import structlog

from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData

logger = structlog.get_logger(__name__)


class SSIMSceneDetector:
    """Rilevatore di cambiamenti di scena basato su SSIM.

    Confronta ogni frame con l'ultimo frame memorizzato calcolando lo
    score SSIM. Se lo score scende sotto la soglia configurata, la scena
    viene considerata cambiata.

    Attributes:
        threshold: Soglia SSIM sotto la quale la scena è considerata cambiata.
            Valori tipici: 0.80–0.90. Più alto = più sensibile ai cambiamenti.
    """

    def __init__(self, threshold: float = 0.85) -> None:
        """Inizializza il detector SSIM.

        Args:
            threshold: Soglia SSIM nell'intervallo (0, 1]. Un frame è
                considerato "cambiato" se SSIM < threshold.
        """
        self.threshold = threshold
        self._last_frame: FrameData | None = None

    def analyze(self, frame: FrameData) -> SceneAnalysis:
        """Analizza un frame calcolando SSIM rispetto al frame precedente.

        Al primo frame (nessun precedente) restituisce sempre
        ``scene_changed=True``.

        Args:
            frame: Frame corrente da analizzare.

        Returns:
            SceneAnalysis con ``ssim_score`` valorizzato e ``scene_changed``
            impostato in base alla soglia configurata.
        """
        # TODO: implementare
        # 1. Se self._last_frame è None → SceneAnalysis(detections=(), scene_changed=True)
        # 2. Decodifica entrambi i frame da bytes con cv2.imdecode
        # 3. Converti in grayscale con cv2.cvtColor
        # 4. Ridimensiona al minore dei due se le dimensioni differiscono
        # 5. Calcola ssim_score con skimage.metrics.structural_similarity
        # 6. scene_changed = ssim_score < self.threshold
        # 7. Aggiorna self._last_frame = frame
        # 8. Logga ssim_score e scene_changed
        # 9. Restituisci SceneAnalysis(detections=(), scene_changed=..., ssim_score=...)
        raise NotImplementedError

    def reset(self) -> None:
        """Resetta il frame di riferimento interno.

        Il prossimo frame analizzato sarà sempre considerato "cambiato".
        """
        self._last_frame = None
        logger.debug("ssim_detector.reset")


__all__ = ["SSIMSceneDetector"]
