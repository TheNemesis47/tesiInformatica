"""Port per la sintesi vocale tramite TTS.

Definisce il contratto per il componente che trasforma testo in audio.
Le implementazioni concrete si trovano in ``adapters.speech``.
"""

from __future__ import annotations

from typing import Protocol

from vision_caption.core.domain.audio import AudioResult


class SpeechSynthesizerPort(Protocol):
    """Interfaccia per la sintesi vocale (Text-to-Speech).

    L'implementazione è asincrona perché la sintesi (Chatterbox Turbo)
    è un'operazione compute-bound su GPU che può richiedere diversi secondi.
    """

    async def synthesize(self, text: str, language: str = "it") -> AudioResult:
        """Sintetizza il testo fornito in audio.

        Args:
            text: Testo da sintetizzare.
            language: Codice lingua ISO 639-1 (es. "it", "en"). Determina
                la voce e la prosodia utilizzate.

        Returns:
            AudioResult con i bytes audio e i metadati di latenza.

        Raises:
            SpeechSynthesisError: Se il modello TTS non è disponibile o
                la sintesi fallisce.
        """
        ...


__all__ = ["SpeechSynthesizerPort"]
