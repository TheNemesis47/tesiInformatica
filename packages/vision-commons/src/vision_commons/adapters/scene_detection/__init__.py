"""Scene detection adapters condivisi."""

from __future__ import annotations

from vision_commons.adapters.scene_detection.hybrid_detector import HybridSceneDetector
from vision_commons.adapters.scene_detection.rfdetr_detector import RFDETRSceneDetector
from vision_commons.adapters.scene_detection.ssim_detector import SSIMSceneDetector

__all__ = ["HybridSceneDetector", "RFDETRSceneDetector", "SSIMSceneDetector"]
