"""Port per la codifica/transcodifica dell'audio.

Definisce il contratto per il componente che converte l'audio da un formato
all'altro (tipicamente da WAV grezzo a Opus compresso per lo streaming).
Le implementazioni concrete si trovano in ``adapters.audio_encoding``.
"""

from __future__ import annotations

from typing import Protocol

from vision_caption.core.domain.audio import AudioFormat, AudioResult


class AudioEncoderPort(Protocol):
    """Interfaccia per la codifica audio.

    Converte un AudioResult da un formato sorgente a un formato di destinazione.
    Tipicamente usato per comprimere WAV → Opus prima dell'invio via WebSocket.
    """

    def encode(self, audio: AudioResult, target_format: AudioFormat) -> AudioResult:
        """Codifica l'audio nel formato di destinazione.

        Args:
            audio: AudioResult sorgente da convertire.
            target_format: Formato di destinazione desiderato.

        Returns:
            Nuovo AudioResult con i bytes nel formato di destinazione.
            Se il formato sorgente è già quello di destinazione, può
            restituire l'input invariato.

        Raises:
            VisionCaptionError: Se la conversione non è supportata o fallisce.
        """
        ...


__all__ = ["AudioEncoderPort"]
