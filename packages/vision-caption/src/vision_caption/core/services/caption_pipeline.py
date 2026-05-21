"""Pipeline principale di audio-descrizione.

Questo è l'orchestratore centrale del sistema. Riceve un frame,
determina se la scena è cambiata, genera una caption testuale,
e la sintetizza in audio. Non ha dipendenze esterne — lavora
esclusivamente tramite i ports iniettati.

Flusso di elaborazione:
    1. Se mode == POINTING → bypassa scene detection, genera subito
    2. Se mode == AUTO → controlla scene change tramite SceneDetector
    3. Controlla rate limiter (min_interval_sec tra caption consecutive)
    4. Genera caption testuale via CaptionGenerator (VLM)
    5. Sintetizza audio via SpeechSynthesizer (TTS)
    6. Logga metriche di latenza per benchmark tesi
"""

from __future__ import annotations

import structlog

from vision_caption.core.domain.audio import AudioResult
from vision_caption.core.domain.caption import CaptionRequest
from vision_commons.domain.frame import CaptureMode, FrameData
from vision_caption.core.ports.caption_generator import CaptionGeneratorPort
from vision_commons.ports.scene_detector import SceneDetectorPort
from vision_caption.core.ports.speech_synthesizer import SpeechSynthesizerPort
from vision_caption.core.services.rate_limiter import RateLimiter

logger = structlog.get_logger(__name__)


class CaptionPipeline:
    """Orchestratore della pipeline di audio-descrizione.

    Coordina scene detection, generazione caption e sintesi vocale
    applicando throttling tramite il rate limiter.

    Attributes:
        _scene_detector: Detector per il cambiamento di scena.
        _caption_generator: Generatore di caption tramite VLM.
        _speech_synthesizer: Sintetizzatore vocale TTS.
        _rate_limiter: Throttler per limitare la frequenza delle caption.
    """

    def __init__(
        self,
        scene_detector: SceneDetectorPort,
        caption_generator: CaptionGeneratorPort,
        speech_synthesizer: SpeechSynthesizerPort,
        rate_limiter: RateLimiter,
    ) -> None:
        """Inizializza la pipeline con le dipendenze iniettate.

        Args:
            scene_detector: Implementazione del port SceneDetectorPort.
            caption_generator: Implementazione del port CaptionGeneratorPort.
            speech_synthesizer: Implementazione del port SpeechSynthesizerPort.
            rate_limiter: Rate limiter per throttling delle caption.
        """
        self._scene_detector = scene_detector
        self._caption_generator = caption_generator
        self._speech_synthesizer = speech_synthesizer
        self._rate_limiter = rate_limiter

    async def process(self, frame: FrameData) -> AudioResult | None:
        """Processa un frame attraverso l'intera pipeline.

        Determina se è necessario generare una nuova caption basandosi
        sulla modalità, sull'analisi del cambiamento di scena e sul rate
        limiter. Se sì, genera la caption e la sintetizza in audio.

        Args:
            frame: Frame da processare.

        Returns:
            AudioResult con l'audio sintetizzato se è stata generata una
            nuova caption, None se il frame non ha determinato una nuova
            descrizione (scena invariata, rate limiting attivo).

        Raises:
            CaptionGenerationError: Se la generazione della caption fallisce.
            SpeechSynthesisError: Se la sintesi vocale fallisce.
        """
        # 1. Se mode == POINTING, bypassa scene detection e delega
        if frame.metadata.mode is CaptureMode.POINTING:
            return await self.process_pointing(frame)

        # 2. Se mode == AUTO, controlla scene change
        analysis = self._scene_detector.analyze(frame)
        if not analysis.scene_changed:
            logger.info(
                "pipeline.scene_stable",
                ssim_score=analysis.ssim_score
            )
            return None

        # 3. Controlla il rate limiter
        if not self._rate_limiter.can_proceed():
            logger.info(
                "pipeline.rate_limited",
                seconds_until_next=self._rate_limiter.seconds_until_next
            )
            return None

        # 4. Registra l'evento
        self._rate_limiter.record()

        # 5. Costruisci CaptionRequest e genera la caption con il VLM
        caption_request = CaptionRequest(frame=frame, mode=frame.metadata.mode)
        caption = await self._caption_generator.generate(caption_request)
        logger.info(
            "pipeline.caption_generated",
            text=caption.text,
            generation_time_ms=caption.generation_time_ms,
        )

        # 6. Sintetizza l'audio con il TTS
        audio_result = await self._speech_synthesizer.synthesize(
            text=caption.text,
            language=caption.language
        )
        logger.info(
            "pipeline.speech_synthesized",
            synthesis_time_ms=audio_result.synthesis_time_ms,
            total_latency_ms=caption.generation_time_ms + audio_result.synthesis_time_ms
        )

        return audio_result

    async def process_pointing(
        self,
        frame: FrameData,
        prompt_override: str | None = None,
    ) -> AudioResult:
        """Processa un frame in modalità POINTING, bypassando il rate limiter.

        Usato quando l'utente indica esplicitamente un punto di interesse:
        la descrizione viene sempre generata indipendentemente dalla scena
        precedente e dal throttling.

        Args:
            frame: Frame da processare, con metadati pointing_coords valorizzati.
            prompt_override: Prompt personalizzato opzionale.

        Returns:
            AudioResult con la descrizione dell'area indicata.

        Raises:
            CaptionGenerationError: Se la generazione della caption fallisce.
            SpeechSynthesisError: Se la sintesi vocale fallisce.
        """
        caption_request = CaptionRequest(
            frame=frame,
            mode=CaptureMode.POINTING,
            prompt_override=prompt_override
        )
        caption = await self._caption_generator.generate(caption_request)
        logger.info(
            "pipeline.pointing.caption_generated",
            text=caption.text,
            generation_time_ms=caption.generation_time_ms,
        )

        audio_result = await self._speech_synthesizer.synthesize(
            text=caption.text,
            language=caption.language
        )
        logger.info(
            "pipeline.pointing.speech_synthesized",
            synthesis_time_ms=audio_result.synthesis_time_ms,
            total_latency_ms=caption.generation_time_ms + audio_result.synthesis_time_ms
        )

        return audio_result


__all__ = ["CaptionPipeline"]
