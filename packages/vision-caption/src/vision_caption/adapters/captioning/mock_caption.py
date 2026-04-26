"""Adapter mock per la generazione di caption, usato nei test.

Restituisce caption predefinite senza richiedere GPU o connessione a Ollama.
Utile per test unitari e di integrazione della pipeline.
"""

from __future__ import annotations

import time

from vision_caption.core.domain.caption import Caption, CaptionRequest
from vision_commons.domain.frame import CaptureMode

_MOCK_CAPTIONS: dict[CaptureMode, str] = {
    CaptureMode.AUTO: (
        "Stanza con scrivania e monitor davanti. "
        "Sedia a rotelle a sinistra, attenzione alla distanza."
    ),
    CaptureMode.POINTING: (
        "Bottiglia d'acqua, a circa mezzo metro. "
        "Etichetta: Acqua naturale."
    ),
}


class MockCaptionGenerator:
    """Generatore di caption mock per test senza GPU.

    Restituisce caption predefinite con un ritardo simulato configurabile.
    Mantiene un contatore delle chiamate per facilitare le asserzioni nei test.

    Attributes:
        simulated_delay_ms: Ritardo simulato in millisecondi (default 0).
        call_count: Numero di chiamate a ``generate()`` dall'istanziazione.
    """

    def __init__(
        self,
        simulated_delay_ms: float = 0.0,
        custom_caption: str | None = None,
    ) -> None:
        """Inizializza il mock generator.

        Args:
            simulated_delay_ms: Ritardo simulato per emulare la latenza GPU.
            custom_caption: Caption personalizzata da restituire per tutte le
                modalità. Se None, usa le caption predefinite per modalità.
        """
        self.simulated_delay_ms = simulated_delay_ms
        self.custom_caption = custom_caption
        self.call_count: int = 0

    async def generate(self, request: CaptionRequest) -> Caption:
        """Restituisce una caption mock senza invocare alcun modello.

        Args:
            request: Richiesta (usata solo per la modalità).

        Returns:
            Caption con testo predefinito e latenza simulata.
        """
        self.call_count += 1
        t0 = time.perf_counter()

        if self.custom_caption is not None:
            text = self.custom_caption
        else:
            text = _MOCK_CAPTIONS.get(request.mode, _MOCK_CAPTIONS[CaptureMode.AUTO])

        generation_time_ms = (time.perf_counter() - t0) * 1000 + self.simulated_delay_ms

        return Caption(
            text=text,
            mode=request.mode,
            language="it",
            generation_time_ms=generation_time_ms,
        )


__all__ = ["MockCaptionGenerator"]
