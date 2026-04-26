"""Test per HybridSceneDetector.

Verifica che il detector ibrido deleghi correttamente a SSIM e RF-DETR
usando mock dei due componenti.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from vision_commons.adapters.scene_detection.hybrid_detector import HybridSceneDetector
from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData


class TestHybridSceneDetector:
    """Test per il rilevatore ibrido SSIM + RF-DETR."""

    def test_skips_rfdetr_when_ssim_stable(self, mock_frame_data: FrameData) -> None:
        """RF-DETR non viene invocato se SSIM indica scena stabile."""
        # TODO: decommentare quando HybridSceneDetector.analyze() è implementato
        # ssim_mock = MagicMock()
        # ssim_mock.analyze.return_value = SceneAnalysis(
        #     detections=(), scene_changed=False, ssim_score=0.97
        # )
        # rfdetr_mock = MagicMock()
        # detector = HybridSceneDetector(ssim_mock, rfdetr_mock)
        # result = detector.analyze(mock_frame_data)
        # assert result.scene_changed is False
        # rfdetr_mock.analyze.assert_not_called()
        pytest.skip("HybridSceneDetector.analyze() non ancora implementato")

    def test_invokes_rfdetr_when_ssim_changed(self, mock_frame_data: FrameData) -> None:
        """RF-DETR viene invocato se SSIM indica cambio di scena."""
        # TODO: decommentare quando HybridSceneDetector.analyze() è implementato
        # ssim_mock = MagicMock()
        # ssim_mock.analyze.return_value = SceneAnalysis(
        #     detections=(), scene_changed=True, ssim_score=0.70
        # )
        # rfdetr_mock = MagicMock()
        # rfdetr_mock.analyze.return_value = SceneAnalysis(
        #     detections=(), scene_changed=True, semantic_diff=0.4
        # )
        # detector = HybridSceneDetector(ssim_mock, rfdetr_mock)
        # result = detector.analyze(mock_frame_data)
        # rfdetr_mock.analyze.assert_called_once()
        pytest.skip("HybridSceneDetector.analyze() non ancora implementato")

    def test_initialization(self) -> None:
        """HybridSceneDetector memorizza i due detector iniettati."""
        ssim_mock = MagicMock()
        rfdetr_mock = MagicMock()
        detector = HybridSceneDetector(ssim_mock, rfdetr_mock)
        assert detector.ssim_detector is ssim_mock
        assert detector.rfdetr_detector is rfdetr_mock
