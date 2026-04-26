"""Adapter mock per la sintesi vocale, usato nei test.

Restituisce bytes audio vuoti senza richiedere GPU o modello TTS.
Utile per test unitari e di integrazione della pipeline.
"""

from __future__ import annotations

import time

from vision_caption.core.domain.audio import AudioFormat, AudioResult


class MockSynthesizer:
    """Sintetizzatore vocale mock per test senza GPU.

    Restituisce AudioResult con bytes vuoti e un ritardo simulato
    configurabile. Mantiene un contatore delle chiamate.

    Attributes:
        simulated_delay_ms: Ritardo simulato in millisecondi (default 0).
        call_count: Numero di chiamate a ``synthesize()`` dall'istanziazione.
        sample_rate: Sample rate dichiarato nell'AudioResult restituito.
    """

    def __init__(
        self,
        simulated_delay_ms: float = 0.0,
        sample_rate: int = 22050,
    ) -> None:
        """Inizializza il mock synthesizer.

        Args:
            simulated_delay_ms: Ritardo simulato per emulare la latenza GPU.
            sample_rate: Sample rate dichiarato nell'AudioResult restituito.
        """
        self.simulated_delay_ms = simulated_delay_ms
        self.sample_rate = sample_rate
        self.call_count: int = 0

    async def synthesize(self, text: str, language: str = "it") -> AudioResult:
        """Restituisce un AudioResult mock senza invocare alcun modello TTS.

        Args:
            text: Testo da sintetizzare (usato solo come caption_text).
            language: Codice lingua (ignorato nel mock).

        Returns:
            AudioResult con bytes vuoti e latenza simulata.
        """
        self.call_count += 1
        t0 = time.perf_counter()
        synthesis_time_ms = (time.perf_counter() - t0) * 1000 + self.simulated_delay_ms

        return AudioResult(
            audio_bytes=b"",
            format=AudioFormat.WAV,
            sample_rate=self.sample_rate,
            duration_ms=0.0,
            caption_text=text,
            synthesis_time_ms=synthesis_time_ms,
        )


__all__ = ["MockSynthesizer"]
