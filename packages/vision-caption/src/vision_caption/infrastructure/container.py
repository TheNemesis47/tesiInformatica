"""Dependency Injection container — assemblaggio di ports e adapters.

Questo modulo è responsabile di costruire il grafo di dipendenze concreto
a partire dalla configurazione. È l'unico posto dell'applicazione in cui
gli adapter concreti vengono istanziati.

Il container segue il pattern Service Locator semplificato: espone metodi
factory che costruiscono e cacheano le istanze.
"""

from __future__ import annotations

import structlog

from vision_caption.adapters.captioning.gemma_caption import GemmaCaptionGenerator
from vision_caption.adapters.captioning.mock_caption import MockCaptionGenerator
from vision_commons.adapters.frame_source.webcam_source import WebcamFrameSource
from vision_commons.adapters.preprocessing.opencv_preprocessor import OpenCVFramePreprocessor
from vision_commons.adapters.scene_detection.hybrid_detector import HybridSceneDetector
from vision_commons.adapters.scene_detection.rfdetr_detector import RFDETRSceneDetector
from vision_commons.adapters.scene_detection.ssim_detector import SSIMSceneDetector
from vision_caption.adapters.speech.chatterbox_synth import ChatterboxSynthesizer
from vision_caption.adapters.speech.mock_synth import MockSynthesizer
from vision_caption.core.ports.caption_generator import CaptionGeneratorPort
from vision_commons.ports.frame_preprocessor import FramePreprocessorPort
from vision_commons.ports.frame_source import FrameSourcePort
from vision_commons.ports.scene_detector import SceneDetectorPort
from vision_caption.core.ports.speech_synthesizer import SpeechSynthesizerPort
from vision_caption.core.services.caption_pipeline import CaptionPipeline
from vision_caption.core.services.rate_limiter import RateLimiter
from vision_caption.infrastructure.config.settings import AppSettings

logger = structlog.get_logger(__name__)


class ApplicationContainer:
    """Container DI che assembla l'intera applicazione.

    Costruisce e caching le istanze dei componenti, iniettando le dipendenze
    in modo esplicito. Ogni metodo factory restituisce la stessa istanza
    (singleton per sessione).

    Attributes:
        settings: Configurazione dell'applicazione.
        use_mocks: Se True, usa adapter mock (senza GPU) al posto di quelli reali.
    """

    def __init__(self, settings: AppSettings, use_mocks: bool = False) -> None:
        """Inizializza il container con la configurazione.

        Args:
            settings: Configurazione caricata da YAML/env.
            use_mocks: Se True, sostituisce Gemma e Chatterbox con mock.
                Usato in test e sviluppo senza GPU.
        """
        self.settings = settings
        self.use_mocks = use_mocks

        # Cache delle istanze
        self._scene_detector: SceneDetectorPort | None = None
        self._caption_generator: CaptionGeneratorPort | None = None
        self._speech_synthesizer: SpeechSynthesizerPort | None = None
        self._frame_source: FrameSourcePort | None = None
        self._frame_preprocessor: FramePreprocessorPort | None = None
        self._rate_limiter: RateLimiter | None = None
        self._pipeline: CaptionPipeline | None = None

        logger.info("container.initialized", use_mocks=use_mocks)

    def create_scene_detector(self) -> SceneDetectorPort:
        """Crea o restituisce il detector di scena configurato.

        Usa HybridSceneDetector (SSIM + RF-DETR) con i parametri da settings.

        Returns:
            Istanza cacheata di SceneDetectorPort.
        """
        if self._scene_detector is None:
            sd = self.settings.scene_detection
            ssim = SSIMSceneDetector(threshold=sd.ssim_threshold)
            rfdetr = RFDETRSceneDetector(
                model_size=sd.rfdetr_model_size,
                confidence_threshold=sd.rfdetr_confidence,
            )
            self._scene_detector = HybridSceneDetector(
                ssim_detector=ssim,
                rfdetr_detector=rfdetr,
            )
            logger.info(
                "container.scene_detector_created",
                ssim_threshold=sd.ssim_threshold,
                rfdetr_model=sd.rfdetr_model_size,
            )
        return self._scene_detector

    def create_caption_generator(self) -> CaptionGeneratorPort:
        """Crea o restituisce il generatore di caption.

        Usa GemmaCaptionGenerator in produzione, MockCaptionGenerator se
        ``use_mocks=True``.

        Returns:
            Istanza cacheata di CaptionGeneratorPort.
        """
        if self._caption_generator is None:
            if self.use_mocks:
                self._caption_generator = MockCaptionGenerator()
                logger.info("container.caption_generator_created", type="mock")
            else:
                vlm = self.settings.vlm
                self._caption_generator = GemmaCaptionGenerator(
                    model_name=vlm.model_name,
                    temperature=vlm.temperature,
                    max_tokens=vlm.max_tokens,
                    language=vlm.language,
                )
                logger.info(
                    "container.caption_generator_created",
                    type="gemma",
                    model=vlm.model_name,
                )
        return self._caption_generator

    def create_speech_synthesizer(self) -> SpeechSynthesizerPort:
        """Crea o restituisce il sintetizzatore vocale.

        Usa ChatterboxSynthesizer in produzione, MockSynthesizer se
        ``use_mocks=True``.

        Returns:
            Istanza cacheata di SpeechSynthesizerPort.
        """
        if self._speech_synthesizer is None:
            if self.use_mocks:
                self._speech_synthesizer = MockSynthesizer()
                logger.info("container.speech_synthesizer_created", type="mock")
            else:
                tts = self.settings.tts
                self._speech_synthesizer = ChatterboxSynthesizer(
                    exaggeration=tts.exaggeration,
                    cfg_weight=tts.cfg_weight,
                )
                logger.info(
                    "container.speech_synthesizer_created",
                    type="chatterbox",
                    model=tts.model,
                )
        return self._speech_synthesizer

    def create_frame_source(self) -> FrameSourcePort:
        """Crea o restituisce la sorgente di frame.

        Usa WebcamFrameSource con la risoluzione configurata.

        Returns:
            Istanza cacheata di FrameSourcePort.
        """
        if self._frame_source is None:
            cam = self.settings.camera
            self._frame_source = WebcamFrameSource(
                resolution=(cam.resolution_width, cam.resolution_height),
            )
            logger.info(
                "container.frame_source_created",
                resolution=f"{cam.resolution_width}x{cam.resolution_height}",
            )
        return self._frame_source

    def create_frame_preprocessor(self) -> FramePreprocessorPort:
        """Crea o restituisce il pre-processore di frame.

        Returns:
            Istanza cacheata di FramePreprocessorPort.
        """
        if self._frame_preprocessor is None:
            self._frame_preprocessor = OpenCVFramePreprocessor()
            logger.info("container.frame_preprocessor_created", type="opencv")
        return self._frame_preprocessor

    def create_rate_limiter(self) -> RateLimiter:
        """Crea o restituisce il rate limiter.

        Returns:
            Istanza cacheata di RateLimiter.
        """
        if self._rate_limiter is None:
            interval = self.settings.scene_detection.min_caption_interval_sec
            self._rate_limiter = RateLimiter(min_interval_sec=interval)
            logger.info("container.rate_limiter_created", interval_sec=interval)
        return self._rate_limiter

    def create_pipeline(self) -> CaptionPipeline:
        """Crea o restituisce la pipeline completa.

        Assembla tutti i componenti iniettandoli nella CaptionPipeline.

        Returns:
            Istanza cacheata di CaptionPipeline pronta all'uso.
        """
        if self._pipeline is None:
            self._pipeline = CaptionPipeline(
                scene_detector=self.create_scene_detector(),
                caption_generator=self.create_caption_generator(),
                speech_synthesizer=self.create_speech_synthesizer(),
                rate_limiter=self.create_rate_limiter(),
            )
            logger.info("container.pipeline_created")
        return self._pipeline


__all__ = ["ApplicationContainer"]
