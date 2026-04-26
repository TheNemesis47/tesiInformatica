"""Fixtures pytest condivise per tutti i test di vision-caption.

Fornisce oggetti di dominio pre-costruiti per evitare duplicazione
nei test unitari e di integrazione.
"""

from __future__ import annotations

import pytest

from vision_caption.core.domain.audio import AudioFormat, AudioResult
from vision_caption.core.domain.caption import Caption, CaptionRequest
from vision_caption.core.domain.detection import BoundingBox, Detection, SceneAnalysis
from vision_caption.core.domain.frame import CaptureMode, FrameData, FrameMetadata
from vision_caption.infrastructure.config.settings import AppSettings

# ── Frame fixtures ─────────────────────────────────────────────────────────


@pytest.fixture
def minimal_jpeg_bytes() -> bytes:
    """Bytes di un'immagine JPEG 1x1 pixel valida.

    Usata come immagine minima per i test senza richiedere file su disco.
    """
    # JPEG 1x1 pixel bianco minimo valido
    return (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t"
        b"\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
        b"\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\x1e\xc0"
        b"\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f"
        b"\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4"
        b"\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04"
        b"\x00\x00\x01}\x01\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa"
        b'\x07"q\x142\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br'
        b"\x82\t\n\x16\x17\x18\x19\x1a%&'()*456789:CDEFGHIJ"
        b"STUVWXYZ\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xf5\x00\x1f\xff\xd9"
    )


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
