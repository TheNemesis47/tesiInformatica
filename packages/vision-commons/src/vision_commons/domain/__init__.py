"""Modelli di dominio condivisi tra vision-caption e object-memory."""

from __future__ import annotations

from vision_commons.domain.detection import BoundingBox, Detection, SceneAnalysis
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata

__all__ = [
    "BoundingBox",
    "CaptureMode",
    "Detection",
    "FrameData",
    "FrameMetadata",
    "SceneAnalysis",
]
