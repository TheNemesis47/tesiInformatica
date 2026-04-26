"""Test per i modelli di dominio — verifica creazione e immutabilità.

Questi test garantiscono che i modelli di dominio siano correttamente
immutabili (frozen dataclass) e che i valori vengano correttamente
inizializzati.
"""

from __future__ import annotations

import dataclasses
import time

import pytest

from vision_caption.core.domain.audio import AudioFormat, AudioResult
from vision_caption.core.domain.caption import Caption, CaptionRequest
from vision_commons.domain.detection import BoundingBox, Detection, SceneAnalysis
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata


class TestFrameMetadata:
    """Test per il modello FrameMetadata."""

    def test_default_values(self) -> None:
        """I valori di default sono corretti."""
        meta = FrameMetadata()
        assert meta.mode == CaptureMode.AUTO
        assert meta.pointing_coords is None
        assert meta.crop_size is None
        assert meta.source_resolution == (1280, 960)

    def test_timestamp_auto_generated(self) -> None:
        """Il timestamp viene generato automaticamente se non fornito."""
        t_before = time.time()
        meta = FrameMetadata()
        t_after = time.time()
        assert t_before <= meta.timestamp <= t_after

    def test_immutability(self) -> None:
        """FrameMetadata è immutabile (frozen=True)."""
        meta = FrameMetadata()
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            meta.mode = CaptureMode.POINTING  # type: ignore[misc]

    def test_pointing_mode(self) -> None:
        """I campi pointing_coords e crop_size vengono valorizzati correttamente."""
        meta = FrameMetadata(
            mode=CaptureMode.POINTING,
            pointing_coords=(0.5, 0.3),
            crop_size=320,
        )
        assert meta.mode == CaptureMode.POINTING
        assert meta.pointing_coords == (0.5, 0.3)
        assert meta.crop_size == 320


class TestFrameData:
    """Test per il modello FrameData."""

    def test_creation(self, mock_frame_data: FrameData) -> None:
        """FrameData viene creato correttamente dalla fixture."""
        assert isinstance(mock_frame_data.image_bytes, bytes)
        assert len(mock_frame_data.image_bytes) > 0

    def test_immutability(self, mock_frame_data: FrameData) -> None:
        """FrameData è immutabile (frozen=True)."""
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            mock_frame_data.image_bytes = b""  # type: ignore[misc]


class TestBoundingBox:
    """Test per il modello BoundingBox."""

    def test_computed_properties(self) -> None:
        """width, height, area e center sono calcolati correttamente."""
        bbox = BoundingBox(x1=10.0, y1=20.0, x2=110.0, y2=70.0)
        assert bbox.width == 100.0
        assert bbox.height == 50.0
        assert bbox.area == 5000.0
        assert bbox.center == (60.0, 45.0)

    def test_immutability(self) -> None:
        """BoundingBox è immutabile."""
        bbox = BoundingBox(x1=0.0, y1=0.0, x2=1.0, y2=1.0)
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            bbox.x1 = 5.0  # type: ignore[misc]


class TestSceneAnalysis:
    """Test per il modello SceneAnalysis."""

    def test_scene_changed(self, mock_scene_analysis: SceneAnalysis) -> None:
        """La fixture di scena cambiata ha scene_changed=True."""
        assert mock_scene_analysis.scene_changed is True
        assert len(mock_scene_analysis.detections) == 1

    def test_stable_scene(self, stable_scene_analysis: SceneAnalysis) -> None:
        """La fixture di scena stabile ha scene_changed=False."""
        assert stable_scene_analysis.scene_changed is False
        assert stable_scene_analysis.ssim_score is not None
        assert stable_scene_analysis.ssim_score > 0.9

    def test_empty_detections(self) -> None:
        """SceneAnalysis può avere detections vuota."""
        analysis = SceneAnalysis(detections=(), scene_changed=False)
        assert analysis.detections == ()


class TestCaption:
    """Test per il modello Caption."""

    def test_creation(self, mock_caption: Caption) -> None:
        """Caption viene creata correttamente dalla fixture."""
        assert mock_caption.language == "it"
        assert mock_caption.mode == CaptureMode.AUTO
        assert len(mock_caption.text) > 0
        assert mock_caption.generation_time_ms > 0

    def test_immutability(self, mock_caption: Caption) -> None:
        """Caption è immutabile."""
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            mock_caption.text = "diverso"  # type: ignore[misc]


class TestAudioResult:
    """Test per il modello AudioResult."""

    def test_format_enum(self) -> None:
        """AudioFormat ha i valori WAV e OPUS."""
        assert AudioFormat.WAV == "wav"
        assert AudioFormat.OPUS == "opus"

    def test_creation(self, mock_audio_result: AudioResult) -> None:
        """AudioResult viene creato correttamente dalla fixture."""
        assert mock_audio_result.format == AudioFormat.WAV
        assert mock_audio_result.sample_rate == 22050

    def test_immutability(self, mock_audio_result: AudioResult) -> None:
        """AudioResult è immutabile."""
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            mock_audio_result.audio_bytes = b"hack"  # type: ignore[misc]
