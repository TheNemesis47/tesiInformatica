"""Port per la generazione di caption testuali tramite VLM.

Definisce il contratto per il componente che trasforma un frame video
in una descrizione testuale. Le implementazioni concrete si trovano
in ``adapters.captioning``.
"""

from __future__ import annotations

from typing import Protocol

from vision_caption.core.domain.caption import Caption, CaptionRequest


class CaptionGeneratorPort(Protocol):
    """Interfaccia per la generazione di caption tramite VLM.

    L'implementazione è asincrona perché la chiamata al VLM (Gemma 4
    via Ollama) è un'operazione I/O-bound che può richiedere centinaia
    di millisecondi.
    """

    async def generate(self, request: CaptionRequest) -> Caption:
        """Genera una caption testuale per il frame contenuto nella richiesta.

        Args:
            request: Richiesta contenente il frame, la modalità e
                un eventuale prompt personalizzato.

        Returns:
            Caption con il testo generato e i metadati di latenza.

        Raises:
            CaptionGenerationError: Se il VLM non è raggiungibile o
                restituisce un errore.
        """
        ...


__all__ = ["CaptionGeneratorPort"]
