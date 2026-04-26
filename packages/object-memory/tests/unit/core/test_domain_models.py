"""Test per i domain model di object-memory."""

from __future__ import annotations

import dataclasses
import time

import pytest

from object_memory.core.domain.object_record import ObjectLabel, ObjectRecord, SpatialPosition
from vision_commons.domain.detection import BoundingBox


class TestObjectLabel:
    def test_immutability(self, mock_object_label: ObjectLabel) -> None:
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            mock_object_label.text = "altro"  # type: ignore[misc]

    def test_timestamp_auto_generated(self) -> None:
        t0 = time.time()
        label = ObjectLabel(text="test")
        assert t0 <= label.assigned_at <= time.time()


class TestSpatialPosition:
    def test_center_normalized(self, mock_spatial_position: SpatialPosition) -> None:
        cx, cy = mock_spatial_position.center_normalized
        assert 0.0 <= cx <= 1.0
        assert 0.0 <= cy <= 1.0

    def test_iou_not_implemented(self, mock_spatial_position: SpatialPosition) -> None:
        with pytest.raises(NotImplementedError):
            mock_spatial_position.iou(mock_spatial_position)


class TestObjectRecord:
    def test_create_new(
        self,
        mock_object_label: ObjectLabel,
        mock_spatial_position: SpatialPosition,
    ) -> None:
        record = ObjectRecord.create_new(mock_object_label, mock_spatial_position, "path/img.jpg")
        assert record.detection_count == 1
        assert record.label.text == "persona in piedi"
        assert len(record.id) == 36  # UUID format

    def test_with_updated_position_is_immutable(
        self,
        mock_object_record: ObjectRecord,
        mock_spatial_position: SpatialPosition,
    ) -> None:
        updated = mock_object_record.with_updated_position(mock_spatial_position, "new.jpg")
        assert updated.id == mock_object_record.id
        assert updated.detection_count == mock_object_record.detection_count + 1
        assert updated is not mock_object_record

    def test_original_unchanged_after_update(
        self,
        mock_object_record: ObjectRecord,
        mock_spatial_position: SpatialPosition,
    ) -> None:
        original_count = mock_object_record.detection_count
        mock_object_record.with_updated_position(mock_spatial_position, "new.jpg")
        assert mock_object_record.detection_count == original_count
