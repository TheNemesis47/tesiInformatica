"""Adapter per l'acquisizione di frame da file video tramite OpenCV.

Legge frame da un file video pre-registrato per test riproducibili
della pipeline senza richiedere una webcam fisica.
"""

from __future__ import annotations

from pathlib import Path

import structlog

from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata

logger = structlog.get_logger(__name__)


class VideoFileFrameSource:
    """Sorgente di frame da file video tramite OpenCV.

    Scorre il video frame per frame. Quando il video termina, ``capture()``
    restituisce None, segnalando la fine dello stream.

    Attributes:
        video_path: Percorso al file video sorgente.
        fps_limit: Limite di FPS per la lettura (None = velocità massima).
    """

    def __init__(
        self,
        video_path: Path | str,
        fps_limit: float | None = None,
    ) -> None:
        """Inizializza la sorgente da file video.

        Args:
            video_path: Percorso al file video (es. MP4, AVI, MKV).
            fps_limit: FPS massimi di lettura. None per leggere alla
                velocità massima del sistema.
        """
        self.video_path = Path(video_path)
        self.fps_limit = fps_limit
        self._cap: object | None = None  # cv2.VideoCapture
        self._frame_count: int = 0

    def capture(self) -> FrameData | None:
        """Legge il prossimo frame dal file video.

        Returns:
            FrameData con il frame corrente, oppure None al termine del video.
        """
        # TODO: implementare
        raise NotImplementedError

    def release(self) -> None:
        """Chiude il file video e rilascia le risorse.

        Dopo questa chiamata, il frame count viene resettato.
        """
        # TODO: implementare
        raise NotImplementedError

    @property
    def frame_count(self) -> int:
        """Numero di frame letti finora."""
        return self._frame_count


__all__ = ["VideoFileFrameSource"]
