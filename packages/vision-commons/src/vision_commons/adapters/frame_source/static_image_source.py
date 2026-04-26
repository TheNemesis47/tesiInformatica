"""Adapter per sorgente di frame da immagine statica, usato negli unit test.

Restituisce sempre lo stesso frame (o una sequenza predefinita) per
test completamente deterministici e riproducibili senza hardware.
"""

from __future__ import annotations

from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata


class StaticImageFrameSource:
    """Sorgente di frame che fornisce immagini statiche predefinite.

    Può essere configurata per restituire sempre lo stesso frame,
    una sequenza ciclica o un numero limitato di frame prima di
    restituire None.

    Attributes:
        frames: Lista di FrameData da restituire in sequenza.
        loop: Se True, ricomincia dalla prima immagine al termine.
        max_captures: Numero massimo di catture prima di restituire None.
            None = illimitato.
    """

    def __init__(
        self,
        frames: list[FrameData],
        loop: bool = False,
        max_captures: int | None = None,
    ) -> None:
        """Inizializza la sorgente statica.

        Args:
            frames: Lista di frame da restituire in sequenza.
            loop: Se True, ricomincia dalla prima immagine al termine.
            max_captures: Limite di catture. None = illimitato.
        """
        if not frames:
            raise ValueError("frames non può essere vuota")
        self.frames = frames
        self.loop = loop
        self.max_captures = max_captures
        self._index: int = 0
        self._total_captures: int = 0

    def capture(self) -> FrameData | None:
        """Restituisce il prossimo frame dalla sequenza.

        Returns:
            FrameData corrente, oppure None se la sequenza è terminata
            o il limite ``max_captures`` è stato raggiunto.
        """
        if self.max_captures is not None and self._total_captures >= self.max_captures:
            return None

        if self._index >= len(self.frames):
            if self.loop:
                self._index = 0
            else:
                return None

        frame = self.frames[self._index]
        self._index += 1
        self._total_captures += 1
        return frame

    def release(self) -> None:
        """Operazione no-op per la sorgente statica.

        Non ci sono risorse hardware da rilasciare.
        """
        pass

    @classmethod
    def from_bytes(
        cls,
        image_bytes: bytes,
        mode: CaptureMode = CaptureMode.AUTO,
        **kwargs: object,
    ) -> "StaticImageFrameSource":
        """Factory: crea una sorgente da un singolo immagine in bytes.

        Args:
            image_bytes: Bytes dell'immagine (JPEG o PNG).
            mode: Modalità di cattura da impostare nei metadati.
            **kwargs: Argomenti aggiuntivi passati al costruttore.

        Returns:
            StaticImageFrameSource con un singolo frame.
        """
        frame = FrameData(
            image_bytes=image_bytes,
            metadata=FrameMetadata(mode=mode),
        )
        return cls(frames=[frame], **kwargs)


__all__ = ["StaticImageFrameSource"]
