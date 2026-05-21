"""Adapter per l'acquisizione di frame da webcam tramite OpenCV.

Usa cv2.VideoCapture per acquisire frame dalla webcam Logitech Brio 4K
(o qualsiasi dispositivo V4L2/DirectShow compatibile).
"""

from __future__ import annotations

import structlog
import cv2

from vision_caption.shared import FrameCaptureError
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata

logger = structlog.get_logger(__name__)


class WebcamFrameSource:
    """Sorgente di frame da webcam tramite OpenCV.

    Apre il dispositivo di acquisizione all'istanziazione e rilascia
    le risorse hardware quando viene chiamato ``release()``.

    Attributes:
        device_id: ID del dispositivo V4L2/DirectShow (0 = prima webcam).
        resolution: Risoluzione richiesta alla webcam come (width, height).
            La webcam può non supportarla e usare la risoluzione più vicina.
    """

    def __init__(
        self,
        device_id: int = 0,
        resolution: tuple[int, int] = (1280, 720),
    ) -> None:
        """Inizializza la sorgente webcam e apre il dispositivo.

        Args:
            device_id: ID del dispositivo (default 0 = prima webcam).
            resolution: Risoluzione desiderata (width, height).
        """
        self.device_id = device_id
        self.resolution = resolution
        self._cap: cv2.VideoCapture | None = None  # cv2.VideoCapture

    def _open(self) -> None:
        """Apre la connessione con il dispositivo di acquisizione.

        Configura la risoluzione e verifica che il dispositivo sia accessibile.

        Raises:
            FrameCaptureError: Se il dispositivo non è disponibile.
        """

        self._cap = cv2.VideoCapture(self.device_id)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        if not self._cap.isOpened():
            raise FrameCaptureError(f"Cannot open camera device {self.device_id}")

    def capture(self) -> FrameData | None:
        """Cattura un singolo frame dalla webcam.

        Returns:
            FrameData con il frame compresso in JPEG, oppure None se
            l'acquisizione fallisce.
        """
        if self._cap is None:
            self._cap = self._open()
        ret, frame = self._cap.read()
        if not ret:
            logger.warning("Failed to acquire frame")
            return None
        compressedFrame = cv2.imencode(".jpg", frame)[1].tobytes()
        metaData = FrameMetadata(
            source_resolution= self.resolution
        )
        return FrameData(
            image_bytes=compressedFrame,
            metadata=metaData
        )

    def release(self) -> None:
        """Rilascia il dispositivo di acquisizione.

        Deve essere chiamato quando la webcam non è più necessaria.
        """

        if self._cap is not None:
            self._cap.release()
            self._cap = None
            logger.info(f"Camera with id:{self.device_id} released")


__all__ = ["WebcamFrameSource"]
