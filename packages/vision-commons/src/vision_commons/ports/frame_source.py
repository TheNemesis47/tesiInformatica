"""Port per la sorgente dei frame video.

Definisce il contratto per il componente che acquisisce frame dalla sorgente
(webcam, file video, immagine statica). Le implementazioni concrete si trovano
in ``adapters.frame_source``.
"""

from __future__ import annotations

from typing import Protocol

from vision_commons.domain.frame import FrameData


class FrameSourcePort(Protocol):
    """Interfaccia per la sorgente di frame video.

    Astrae il dispositivo di acquisizione (webcam Brio 4K, Meta Quest 3,
    file video) permettendo di sostituirlo senza modificare la pipeline.
    """

    def capture(self) -> FrameData | None:
        """Cattura un singolo frame dalla sorgente.

        Returns:
            FrameData con il frame acquisito, oppure None se la sorgente
            non è pronta o ha esaurito i frame disponibili (es. fine video).
        """
        ...

    def release(self) -> None:
        """Rilascia le risorse hardware della sorgente.

        Deve essere chiamato quando la sorgente non è più necessaria,
        per liberare la camera o chiudere il file video.
        """
        ...


__all__ = ["FrameSourcePort"]
