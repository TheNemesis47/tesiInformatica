"""Test per OverlapTracker.

I metodi find_matching_record e should_update_snapshot sono TODO,
quindi questi test verificano solo la costruzione e i parametri di default.
Quando i metodi saranno implementati si potranno decommentare i test completi.
"""

from __future__ import annotations

import pytest

from object_memory.core.services.overlap_tracker import OverlapTracker


class TestOverlapTrackerInit:
    def test_default_thresholds(self) -> None:
        tracker = OverlapTracker()
        assert tracker.iou_threshold == 0.4
        assert tracker.position_update_threshold == 0.15

    def test_custom_thresholds(self) -> None:
        tracker = OverlapTracker(iou_threshold=0.6, position_update_threshold=0.25)
        assert tracker.iou_threshold == 0.6
        assert tracker.position_update_threshold == 0.25

    def test_zero_iou_threshold(self) -> None:
        """Con soglia 0 qualsiasi overlap matcha — costruzione valida."""
        tracker = OverlapTracker(iou_threshold=0.0)
        assert tracker.iou_threshold == 0.0

    def test_full_iou_threshold(self) -> None:
        """Soglia 1 richiede overlap perfetto — costruzione valida."""
        tracker = OverlapTracker(iou_threshold=1.0)
        assert tracker.iou_threshold == 1.0


class TestOverlapTrackerFindMatch:
    def test_find_matching_record_not_implemented(
        self,
        mock_detection: object,
        mock_object_record: object,
    ) -> None:
        """Verifica che il metodo sollevi NotImplementedError finché non è implementato."""
        tracker = OverlapTracker()
        with pytest.raises(NotImplementedError):
            tracker.find_matching_record(
                detection=mock_detection,  # type: ignore[arg-type]
                frame_width=1280,
                frame_height=960,
                known_records=[mock_object_record],  # type: ignore[list-item]
            )

    def test_find_matching_record_empty_catalog_not_implemented(
        self,
        mock_detection: object,
    ) -> None:
        """Catalogo vuoto — ancora NotImplementedError."""
        tracker = OverlapTracker()
        with pytest.raises(NotImplementedError):
            tracker.find_matching_record(
                detection=mock_detection,  # type: ignore[arg-type]
                frame_width=1280,
                frame_height=960,
                known_records=[],
            )


class TestOverlapTrackerShouldUpdate:
    def test_should_update_snapshot_not_implemented(
        self,
        mock_spatial_position: object,
        mock_object_record: object,
    ) -> None:
        """Verifica che il metodo sollevi NotImplementedError finché non è implementato."""
        tracker = OverlapTracker()
        with pytest.raises(NotImplementedError):
            tracker.should_update_snapshot(
                new_position=mock_spatial_position,  # type: ignore[arg-type]
                record=mock_object_record,  # type: ignore[arg-type]
            )
