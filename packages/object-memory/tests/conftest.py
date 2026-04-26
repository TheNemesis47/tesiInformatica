"""Fixtures pytest per object-memory."""

from __future__ import annotations

import pytest

from object_memory.core.domain.object_record import ObjectLabel, ObjectRecord, SpatialPosition
from object_memory.core.domain.snapshot import ObjectSnapshot, SnapshotQuery
from object_memory.infrastructure.config.settings import AppSettings
from vision_commons.domain.detection import BoundingBox, Detection, SceneAnalysis
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata


@pytest.fixture
def minimal_jpeg_bytes() -> bytes:
    """JPEG 1x1 pixel bianco per test."""
    return (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        b"\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t"
        b"\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a"
        b"\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\x1e\xc0"
        b"\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xf5\x00\x1f\xff\xd9"
    )


@pytest.fixture
def mock_frame_data(minimal_jpeg_bytes: bytes) -> FrameData:
    """FrameData minimo per test."""
    return FrameData(
        image_bytes=minimal_jpeg_bytes,
        metadata=FrameMetadata(timestamp=1712345678.0, source_resolution=(1280, 960)),
    )


@pytest.fixture
def mock_detection() -> Detection:
    """Detection di una persona per test."""
    return Detection(
        class_name="person",
        confidence=0.88,
        bbox=BoundingBox(x1=100.0, y1=50.0, x2=300.0, y2=480.0),
    )


@pytest.fixture
def mock_spatial_position(mock_detection: Detection) -> SpatialPosition:
    """SpatialPosition derivata dalla mock_detection."""
    return SpatialPosition(
        bbox=mock_detection.bbox,
        frame_width=1280,
        frame_height=960,
        timestamp=1712345678.0,
    )


@pytest.fixture
def mock_object_label() -> ObjectLabel:
    """ObjectLabel di test."""
    return ObjectLabel(text="persona in piedi", language="it", confidence=None)


@pytest.fixture
def mock_object_record(
    mock_object_label: ObjectLabel,
    mock_spatial_position: SpatialPosition,
) -> ObjectRecord:
    """ObjectRecord di test."""
    return ObjectRecord.create_new(
        label=mock_object_label,
        position=mock_spatial_position,
        snapshot_path="mock://test/1.jpg",
    )


@pytest.fixture
def app_settings() -> AppSettings:
    """AppSettings con valori di default per test."""
    return AppSettings()
