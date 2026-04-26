"""Port condivisi — contratti per i componenti riusabili tra i progetti."""

from __future__ import annotations

from vision_commons.ports.frame_preprocessor import FramePreprocessorPort
from vision_commons.ports.frame_source import FrameSourcePort
from vision_commons.ports.scene_detector import SceneDetectorPort

__all__ = ["FramePreprocessorPort", "FrameSourcePort", "SceneDetectorPort"]
