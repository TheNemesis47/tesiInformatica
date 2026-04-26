"""Port per il pre-processing dei frame video.

Definisce il contratto per il componente che prepara i frame prima dell'analisi:
resize, crop, compressione JPEG. Le implementazioni concrete si trovano
in ``adapters.preprocessing``.
"""

from __future__ import annotations

from typing import Protocol

from vision_commons.domain.frame import FrameData


class FramePreprocessorPort(Protocol):
    """Interfaccia per la pre-elaborazione dei frame.

    Ogni operazione di trasformazione restituisce un nuovo FrameData
    (rispettando l'immutabilità dei domain model) senza modificare l'input.
    """

    def resize(self, frame: FrameData, target_size: tuple[int, int]) -> FrameData:
        """Ridimensiona il frame alla dimensione target.

        Args:
            frame: Frame sorgente da ridimensionare.
            target_size: Dimensione desiderata come (width, height) in pixel.

        Returns:
            Nuovo FrameData con l'immagine ridimensionata.
        """
        ...

    def crop_center(self, frame: FrameData, crop_size: int) -> FrameData:
        """Ritaglia un'area quadrata dal centro del frame.

        Args:
            frame: Frame sorgente da ritagliare.
            crop_size: Lato del quadrato di crop in pixel.

        Returns:
            Nuovo FrameData con l'area centrale ritagliata.
        """
        ...

    def crop_at(
        self,
        frame: FrameData,
        center: tuple[float, float],
        crop_size: int,
    ) -> FrameData:
        """Ritaglia un'area quadrata centrata su coordinate normalizzate.

        Usato in modalità POINTING per ritagliare l'area indicata dall'utente.

        Args:
            frame: Frame sorgente da ritagliare.
            center: Centro del crop come coordinate normalizzate (x, y)
                nell'intervallo [0, 1].
            crop_size: Lato del quadrato di crop in pixel.

        Returns:
            Nuovo FrameData con l'area ritagliata centrata sul punto indicato.
        """
        ...

    def encode_jpeg(self, frame: FrameData, quality: int = 75) -> bytes:
        """Comprime l'immagine del frame in formato JPEG.

        Args:
            frame: Frame da comprimere.
            quality: Qualità JPEG nell'intervallo [0, 100].
                Valori bassi = file più piccoli, qualità inferiore.

        Returns:
            Bytes dell'immagine compressa in formato JPEG.
        """
        ...


__all__ = ["FramePreprocessorPort"]
