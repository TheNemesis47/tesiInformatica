"""Adapter per la sintesi vocale tramite Chatterbox TTS API.

Invece di caricare il modello pesante in memoria, questo adapter fa richieste
HTTP al microservizio Chatterbox che è già in esecuzione sulla porta 4123.
"""

from __future__ import annotations

import time

import httpx
import structlog

from vision_caption.core.domain.audio import AudioFormat, AudioResult

logger = structlog.get_logger(__name__)


class ChatterboxSynthesizer:
    """Sintetizzatore vocale tramite Chatterbox TTS API esterna.
    
    Effettua richieste HTTP al server Chatterbox.
    
    Attributes:
        api_url: L'URL base dell'API (es. "http://localhost:4123")
    """

    def __init__(self, api_url: str = "http://localhost:4123") -> None:
        """Inizializza l'adapter.

        Args:
            api_url: URL dell'API di ChatterboxTTS.
        """
        self.api_url = api_url.rstrip("/")
        # Endpoint tipico per la generazione è /audio/speech
        self.endpoint = f"{self.api_url}/v1/audio/speech"

    async def synthesize(self, text: str, language: str = "it") -> AudioResult:
        """Sintetizza il testo in audio tramite l'API di Chatterbox.

        Args:
            text: Testo da sintetizzare.
            language: Codice lingua.

        Returns:
            AudioResult con i bytes WAV e i metadati di latenza.

        Raises:
            Exception: Se l'API restituisce un errore.
        """

        async with httpx.AsyncClient() as client:
            body = {
                "input": text,
                "voice": "default",
                "language": language,
                "speed": 1.2,
            }

            t0 = time.perf_counter()
            try:
                response = await client.post(self.endpoint, json=body, timeout=120)
                response.raise_for_status()
            except Exception as e:
                logger.error("chatterbox.syntesis_failed", error = str(e))
                raise e
            t1 = time.perf_counter()

            audio_bytes = response.content

            logger.info(
                "chatterbox.synthesis_done",
                time_ms=(t1 - t0) * 1000,
                audio_size_bytes=len(audio_bytes),
                text=text,
            )

            return AudioResult(
                audio_bytes=audio_bytes,
                format=AudioFormat.WAV,
                sample_rate=24000,
                duration_ms=0,
                caption_text=text,
                synthesis_time_ms=(t1-t0)*1000
            )

__all__ = ["ChatterboxSynthesizer"]
