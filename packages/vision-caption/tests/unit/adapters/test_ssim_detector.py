"""Test per SSIMSceneDetector.

Questi test verificano il comportamento del detector SSIM senza richiedere
hardware specifico, usando immagini JPEG minimali.
"""

from __future__ import annotations

import pytest

from vision_commons.adapters.scene_detection.ssim_detector import SSIMSceneDetector
from vision_commons.domain.frame import FrameData


class TestSSIMSceneDetector:
    """Test per il rilevatore SSIM."""

    def test_first_frame_always_changed(self, mock_frame_data: FrameData) -> None:
        """Il primo frame analizzato è sempre considerato 'cambiato'."""
        # TODO: decommentare quando SSIMSceneDetector.analyze() è implementato
        # detector = SSIMSceneDetector(threshold=0.85)
        # result = detector.analyze(mock_frame_data)
        # assert result.scene_changed is True
        pytest.skip("SSIMSceneDetector.analyze() non ancora implementato")

    def test_same_frame_not_changed(self, mock_frame_data: FrameData) -> None:
        """Lo stesso frame non produce un cambio di scena."""
        # TODO: decommentare quando SSIMSceneDetector.analyze() è implementato
        # detector = SSIMSceneDetector(threshold=0.85)
        # detector.analyze(mock_frame_data)  # primo frame
        # result = detector.analyze(mock_frame_data)  # stesso frame
        # assert result.scene_changed is False
        # assert result.ssim_score is not None
        # assert result.ssim_score > 0.99
        pytest.skip("SSIMSceneDetector.analyze() non ancora implementato")

    def test_reset_makes_next_frame_changed(self, mock_frame_data: FrameData) -> None:
        """Dopo reset(), il prossimo frame è sempre 'cambiato'."""
        # TODO: decommentare quando SSIMSceneDetector.analyze() è implementato
        # detector = SSIMSceneDetector(threshold=0.85)
        # detector.analyze(mock_frame_data)
        # detector.reset()
        # result = detector.analyze(mock_frame_data)
        # assert result.scene_changed is True
        pytest.skip("SSIMSceneDetector.analyze() non ancora implementato")

    def test_threshold_configuration(self) -> None:
        """La soglia viene impostata correttamente."""
        detector = SSIMSceneDetector(threshold=0.90)
        assert detector.threshold == 0.90
