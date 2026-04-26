"""Modelli di dominio per l'audio sintetizzato dal TTS.

Definisce il formato audio supportato e il risultato della sintesi vocale,
con metadati di latenza per il benchmark della tesi.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AudioFormat(str, Enum):
    """Formato di codifica dell'audio prodotto.

    Attributes:
        WAV: PCM non compresso — alta qualità, file grandi.
            Usato come formato intermedio prima dell'encoding.
        OPUS: Codec Opus — alta qualità, bassa latenza, adatto allo streaming
            via WebSocket. Formato di output finale verso il client.
    """

    WAV = "wav"
    OPUS = "opus"


@dataclass(frozen=True)
class AudioResult:
    """Risultato della sintesi vocale di una caption.

    Contiene i bytes audio pronti per essere inviati al client tramite
    WebSocket, insieme ai metadati necessari per la riproduzione e
    per il benchmark della latenza.

    Attributes:
        audio_bytes: Bytes del file audio nel formato specificato.
        format: Formato di codifica dell'audio.
        sample_rate: Frequenza di campionamento in Hz (es. 22050, 44100).
        duration_ms: Durata dell'audio in millisecondi.
        caption_text: Testo originale che è stato sintetizzato.
            Utile per log e debug senza dover decodificare l'audio.
        synthesis_time_ms: Tempo impiegato per la sintesi in millisecondi.
            Usato per il benchmark della tesi.
    """

    audio_bytes: bytes
    format: AudioFormat
    sample_rate: int
    duration_ms: float
    caption_text: str
    synthesis_time_ms: float


__all__ = ["AudioFormat", "AudioResult"]
