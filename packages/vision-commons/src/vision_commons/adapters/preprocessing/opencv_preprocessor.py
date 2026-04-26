"""Adapter per il pre-processing dei frame tramite OpenCV.

Implementa le operazioni di trasformazione del frame (resize, crop, JPEG)
usando OpenCV. Ogni operazione restituisce un nuovo FrameData immutabile.
"""

from __future__ import annotations

import structlog

from vision_commons.domain.frame import FrameData, FrameMetadata

logger = structlog.get_logger(__name__)


class OpenCVFramePreprocessor:
    """Pre-elaboratore di frame basato su OpenCV.

    Tutte le operazioni sono pure (nessun side effect): ricevono un FrameData
    in input e restituiscono un nuovo FrameData con l'immagine trasformata,
    senza modificare l'originale.
    """

    def resize(self, frame: FrameData, target_size: tuple[int, int]) -> FrameData:
        """Ridimensiona il frame alla dimensione target usando interpolazione INTER_AREA.

        Args:
            frame: Frame sorgente da ridimensionare.
            target_size: Dimensione desiderata (width, height) in pixel.

        Returns:
            Nuovo FrameData con l'immagine ridimensionata.
        """
        # TODO: implementare
        # import cv2, numpy as np
        # 1. Decodifica bytes → np.ndarray con cv2.imdecode
        # 2. Ridimensiona con cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
        # 3. Ricodifica in JPEG con cv2.imencode
        # 4. Aggiorna FrameMetadata.source_resolution
        # 5. Restituisci nuovo FrameData
        raise NotImplementedError

    def crop_center(self, frame: FrameData, crop_size: int) -> FrameData:
        """Ritaglia un'area quadrata dal centro del frame.

        Args:
            frame: Frame sorgente da ritagliare.
            crop_size: Lato del quadrato di crop in pixel.

        Returns:
            Nuovo FrameData con l'area centrale ritagliata.
        """
        # TODO: implementare
        raise NotImplementedError

    def crop_at(
        self,
        frame: FrameData,
        center: tuple[float, float],
        crop_size: int,
    ) -> FrameData:
        """Ritaglia un'area quadrata centrata su coordinate normalizzate.

        Args:
            frame: Frame sorgente da ritagliare.
            center: Centro normalizzato (x, y) in [0, 1].
            crop_size: Lato del quadrato di crop in pixel.

        Returns:
            Nuovo FrameData con l'area ritagliata.
        """
        # TODO: implementare
        raise NotImplementedError

    def encode_jpeg(self, frame: FrameData, quality: int = 75) -> bytes:
        """Comprime l'immagine del frame in formato JPEG.

        Args:
            frame: Frame da comprimere.
            quality: Qualità JPEG [0, 100].

        Returns:
            Bytes JPEG compressi.
        """
        # TODO: implementare
        # import cv2, numpy as np
        # 1. Decodifica bytes → np.ndarray
        # 2. Codifica con cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        # 3. Restituisci jpeg_bytes.tobytes()
        raise NotImplementedError


__all__ = ["OpenCVFramePreprocessor"]
