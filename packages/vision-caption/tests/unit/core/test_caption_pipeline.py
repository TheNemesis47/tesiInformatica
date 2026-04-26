"""Test per la CaptionPipeline con adapter mock.

Verifica la logica di orchestrazione della pipeline senza richiedere
GPU o modelli AI reali.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from vision_caption.core.domain.audio import AudioFormat, AudioResult
from vision_caption.core.domain.caption import Caption
from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import CaptureMode, FrameData
from vision_caption.core.services.caption_pipeline import CaptionPipeline
from vision_caption.core.services.rate_limiter import RateLimiter


@pytest.fixture
def mock_scene_detector_changed() -> MagicMock:
    """SceneDetector mock che indica sempre scena cambiata."""
    detector = MagicMock()
    detector.analyze.return_value = SceneAnalysis(
        detections=(),
        scene_changed=True,
        ssim_score=0.7,
    )
    return detector


@pytest.fixture
def mock_scene_detector_stable() -> MagicMock:
    """SceneDetector mock che indica scena stabile."""
    detector = MagicMock()
    detector.analyze.return_value = SceneAnalysis(
        detections=(),
        scene_changed=False,
        ssim_score=0.98,
    )
    return detector


@pytest.fixture
def mock_caption_gen() -> AsyncMock:
    """CaptionGenerator mock asincrono."""
    gen = AsyncMock()
    gen.generate.return_value = Caption(
        text="Test caption",
        mode=CaptureMode.AUTO,
        language="it",
        generation_time_ms=100.0,
    )
    return gen


@pytest.fixture
def mock_speech_synth() -> AsyncMock:
    """SpeechSynthesizer mock asincrono."""
    synth = AsyncMock()
    synth.synthesize.return_value = AudioResult(
        audio_bytes=b"audio",
        format=AudioFormat.WAV,
        sample_rate=22050,
        duration_ms=500.0,
        caption_text="Test caption",
        synthesis_time_ms=200.0,
    )
    return synth


class TestCaptionPipeline:
    """Test per la logica di orchestrazione della CaptionPipeline."""

    @pytest.mark.asyncio
    async def test_process_returns_none_on_stable_scene(
        self,
        mock_scene_detector_stable: MagicMock,
        mock_caption_gen: AsyncMock,
        mock_speech_synth: AsyncMock,
        mock_frame_data: FrameData,
    ) -> None:
        """process() restituisce None se la scena non è cambiata."""
        pipeline = CaptionPipeline(
            scene_detector=mock_scene_detector_stable,
            caption_generator=mock_caption_gen,
            speech_synthesizer=mock_speech_synth,
            rate_limiter=RateLimiter(min_interval_sec=0.0),
        )
        # TODO: decommentare quando process() è implementato
        # result = await pipeline.process(mock_frame_data)
        # assert result is None
        # mock_caption_gen.generate.assert_not_called()
        pytest.skip("CaptionPipeline.process() non ancora implementato")

    @pytest.mark.asyncio
    async def test_process_generates_audio_on_scene_change(
        self,
        mock_scene_detector_changed: MagicMock,
        mock_caption_gen: AsyncMock,
        mock_speech_synth: AsyncMock,
        mock_frame_data: FrameData,
    ) -> None:
        """process() genera audio quando la scena è cambiata."""
        pipeline = CaptionPipeline(
            scene_detector=mock_scene_detector_changed,
            caption_generator=mock_caption_gen,
            speech_synthesizer=mock_speech_synth,
            rate_limiter=RateLimiter(min_interval_sec=0.0),
        )
        # TODO: decommentare quando process() è implementato
        # result = await pipeline.process(mock_frame_data)
        # assert result is not None
        # assert result.audio_bytes == b"audio"
        # mock_caption_gen.generate.assert_called_once()
        # mock_speech_synth.synthesize.assert_called_once()
        pytest.skip("CaptionPipeline.process() non ancora implementato")

    @pytest.mark.asyncio
    async def test_process_rate_limited(
        self,
        mock_scene_detector_changed: MagicMock,
        mock_caption_gen: AsyncMock,
        mock_speech_synth: AsyncMock,
        mock_frame_data: FrameData,
    ) -> None:
        """process() restituisce None se il rate limiter blocca."""
        rate_limiter = RateLimiter(min_interval_sec=60.0)
        rate_limiter.record()  # Simula evento recente

        pipeline = CaptionPipeline(
            scene_detector=mock_scene_detector_changed,
            caption_generator=mock_caption_gen,
            speech_synthesizer=mock_speech_synth,
            rate_limiter=rate_limiter,
        )
        # TODO: decommentare quando process() è implementato
        # result = await pipeline.process(mock_frame_data)
        # assert result is None
        pytest.skip("CaptionPipeline.process() non ancora implementato")
