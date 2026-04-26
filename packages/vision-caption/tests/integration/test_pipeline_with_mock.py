"""Test di integrazione della pipeline con adapter mock.

Verifica il flusso end-to-end della pipeline usando MockCaptionGenerator
e MockSynthesizer, senza richiedere GPU o modelli AI.
"""

from __future__ import annotations

import pytest

from vision_caption.adapters.captioning.mock_caption import MockCaptionGenerator
from vision_caption.adapters.speech.mock_synth import MockSynthesizer
from vision_commons.domain.frame import CaptureMode, FrameData
from vision_caption.core.services.caption_pipeline import CaptionPipeline
from vision_caption.core.services.rate_limiter import RateLimiter


@pytest.fixture
def pipeline_with_mocks() -> CaptionPipeline:
    """Pipeline completamente mock, nessun hardware richiesto."""
    from unittest.mock import MagicMock
    from vision_commons.domain.detection import SceneAnalysis

    scene_detector = MagicMock()
    scene_detector.analyze.return_value = SceneAnalysis(
        detections=(), scene_changed=True, ssim_score=0.6
    )

    return CaptionPipeline(
        scene_detector=scene_detector,
        caption_generator=MockCaptionGenerator(),
        speech_synthesizer=MockSynthesizer(),
        rate_limiter=RateLimiter(min_interval_sec=0.0),
    )


class TestPipelineWithMocks:
    """Test end-to-end della pipeline con mock adapter."""

    @pytest.mark.asyncio
    async def test_full_pipeline_returns_audio(
        self,
        pipeline_with_mocks: CaptionPipeline,
        mock_frame_data: FrameData,
    ) -> None:
        """La pipeline completa restituisce un AudioResult con mock."""
        # TODO: decommentare quando CaptionPipeline.process() è implementato
        # result = await pipeline_with_mocks.process(mock_frame_data)
        # assert result is not None
        # assert isinstance(result.audio_bytes, bytes)
        # assert len(result.caption_text) > 0
        pytest.skip("CaptionPipeline.process() non ancora implementato")

    @pytest.mark.asyncio
    async def test_mock_generators_call_counts(
        self,
        mock_frame_data: FrameData,
    ) -> None:
        """I mock mantengono correttamente i contatori delle chiamate."""
        from unittest.mock import MagicMock
        from vision_commons.domain.detection import SceneAnalysis

        scene_detector = MagicMock()
        scene_detector.analyze.return_value = SceneAnalysis(
            detections=(), scene_changed=True
        )
        caption_gen = MockCaptionGenerator()
        speech_synth = MockSynthesizer()

        pipeline = CaptionPipeline(
            scene_detector=scene_detector,
            caption_generator=caption_gen,
            speech_synthesizer=speech_synth,
            rate_limiter=RateLimiter(min_interval_sec=0.0),
        )

        assert caption_gen.call_count == 0
        assert speech_synth.call_count == 0

        # TODO: decommentare quando process() è implementato
        # await pipeline.process(mock_frame_data)
        # assert caption_gen.call_count == 1
        # assert speech_synth.call_count == 1
        pytest.skip("CaptionPipeline.process() non ancora implementato")
