"""Fixtures pytest condivise per tutti i test di vision-caption.

Fornisce oggetti di dominio pre-costruiti per evitare duplicazione
nei test unitari e di integrazione.
"""

from __future__ import annotations

import pytest

from vision_caption.core.domain.audio import AudioFormat, AudioResult
from vision_caption.core.domain.caption import Caption, CaptionRequest
from vision_commons.domain.detection import BoundingBox, Detection, SceneAnalysis
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata
from vision_caption.infrastructure.config.settings import AppSettings

# ── Frame fixtures ─────────────────────────────────────────────────────────


@pytest.fixture
def minimal_jpeg_bytes() -> bytes:
    """Genera in memoria i byte di un'immagine JPEG bianca di 100x100 pixel per i test."""
    import cv2
    import numpy as np

    img = np.ones((100, 100), dtype=np.uint8) * 255
    success, encoded_image = cv2.imencode(".jpg", img)
    if not success:
        raise AssertionError("Failed to encode JPEG")
    return encoded_image.tobytes()


@pytest.fixture
def frame_metadata() -> FrameMetadata:
    """FrameMetadata con valori di default per test."""
    return FrameMetadata(
        timestamp=1712345678.0,
        mode=CaptureMode.AUTO,
        source_resolution=(1280, 960),
    )


@pytest.fixture
def mock_frame_data(minimal_jpeg_bytes: bytes, frame_metadata: FrameMetadata) -> FrameData:
    """FrameData minimo per test della pipeline."""
    return FrameData(
        image_bytes=minimal_jpeg_bytes,
        metadata=frame_metadata,
    )


@pytest.fixture
def pointing_frame_data(minimal_jpeg_bytes: bytes) -> FrameData:
    """FrameData in modalità POINTING con coordinate di puntamento."""
    return FrameData(
        image_bytes=minimal_jpeg_bytes,
        metadata=FrameMetadata(
            timestamp=1712345678.0,
            mode=CaptureMode.POINTING,
            pointing_coords=(0.5, 0.5),
            crop_size=320,
            source_resolution=(1280, 960),
        ),
    )


# ── Detection fixtures ─────────────────────────────────────────────────────


@pytest.fixture
def mock_scene_analysis() -> SceneAnalysis:
    """SceneAnalysis con un cambio di scena rilevato."""
    return SceneAnalysis(
        detections=(
            Detection(
                class_name="person",
                confidence=0.92,
                bbox=BoundingBox(x1=100.0, y1=50.0, x2=300.0, y2=480.0),
            ),
        ),
        scene_changed=True,
        ssim_score=0.72,
        semantic_diff=0.45,
        timestamp=1712345678.0,
    )


@pytest.fixture
def stable_scene_analysis() -> SceneAnalysis:
    """SceneAnalysis senza cambio di scena (scena stabile)."""
    return SceneAnalysis(
        detections=(),
        scene_changed=False,
        ssim_score=0.97,
        semantic_diff=0.02,
        timestamp=1712345678.0,
    )


# ── Caption fixtures ────────────────────────────────────────────────────────


@pytest.fixture
def mock_caption() -> Caption:
    """Caption di test generata in modalità AUTO."""
    return Caption(
        text="Scrivania con monitor davanti. Sedia a sinistra.",
        mode=CaptureMode.AUTO,
        language="it",
        generation_time_ms=245.7,
        timestamp=1712345678.5,
    )


# ── Audio fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def mock_audio_result() -> AudioResult:
    """AudioResult con bytes vuoti per test senza TTS."""
    return AudioResult(
        audio_bytes=b"",
        format=AudioFormat.WAV,
        sample_rate=22050,
        duration_ms=1250.0,
        caption_text="Scrivania con monitor davanti. Sedia a sinistra.",
        synthesis_time_ms=890.3,
    )


# ── Settings fixtures ───────────────────────────────────────────────────────


@pytest.fixture
def app_settings() -> AppSettings:
    """AppSettings con valori di default per test."""
    return AppSettings()
