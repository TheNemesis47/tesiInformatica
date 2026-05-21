"""Adapter per il rilevamento di cambiamenti di scena tramite SSIM.

Usa l'indice di similarità strutturale (Structural Similarity Index Measure)
di scikit-image per confrontare il frame corrente con il precedente.
SSIM è veloce e sensibile a cambiamenti di illuminazione e movimento.
"""

from __future__ import annotations

import cv2
import numpy as np
import structlog

from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData
from skimage.metrics import structural_similarity as ssim

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

        if self._last_frame is None:
            self._last_frame = frame
            return SceneAnalysis(detections=(), scene_changed=True)

        #decodifica Frame
        arr_attuale = np.frombuffer(frame.image_bytes, dtype=np.uint8)
        img_attuale = cv2.imdecode(arr_attuale, cv2.IMREAD_GRAYSCALE)

        arr_precedente = np.frombuffer(self._last_frame.image_bytes, dtype=np.uint8)
        img_precedente = cv2.imdecode(arr_precedente, cv2.IMREAD_GRAYSCALE)

        #ridimensionamento
        if img_precedente.shape != img_attuale.shape:
            (altezza_precedente, larghezza_precedente) = img_precedente.shape
            (altezza_attuale, larghezza_attuale) = img_attuale.shape
            nuova_altezza = min(altezza_precedente, altezza_attuale)
            nuova_larghezza = min(larghezza_precedente, larghezza_attuale)
            img_precedente = cv2.resize(img_precedente, (nuova_larghezza, nuova_altezza))
            img_attuale = cv2.resize(img_attuale, (nuova_larghezza, nuova_altezza))

        #delta di scikit
        ssim_score = float(ssim(img_precedente, img_attuale))
        scene_changed = (ssim_score < self.threshold)
        self._last_frame = frame
        logger.info(
            "ssim.analysis_done",
            ssim_score=ssim_score,
            threshold=self.threshold,
            scene_changed=scene_changed
        )
        return SceneAnalysis(detections=(), scene_changed=scene_changed, ssim_score=ssim_score)

    def reset(self) -> None:
        """Resetta il frame di riferimento interno.

        Il prossimo frame analizzato sarà sempre considerato "cambiato".
        """
        self._last_frame = None
        logger.debug("ssim_detector.reset")


__all__ = ["SSIMSceneDetector"]
