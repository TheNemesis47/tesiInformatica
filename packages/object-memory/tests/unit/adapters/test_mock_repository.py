"""Test per il MockObjectRepository."""

from __future__ import annotations

import pytest

from object_memory.adapters.repository.mock_repository import MockObjectRepository
from object_memory.core.domain.snapshot import SnapshotQuery


class TestMockObjectRepository:
    @pytest.mark.asyncio
    async def test_save_and_get(self, mock_object_record: object) -> None:
        repo = MockObjectRepository()
        await repo.save(mock_object_record)
        result = await repo.get_by_id(mock_object_record.id)
        assert result is not None
        assert result.id == mock_object_record.id

    @pytest.mark.asyncio
    async def test_find_by_label_partial_match(self, mock_object_record: object) -> None:
        repo = MockObjectRepository()
        await repo.save(mock_object_record)
        query = SnapshotQuery(query_text="persona")
        results = await repo.find_by_label(query)
        assert len(results) == 1
        assert "persona" in results[0].label.text

    @pytest.mark.asyncio
    async def test_find_no_match(self, mock_object_record: object) -> None:
        repo = MockObjectRepository()
        await repo.save(mock_object_record)
        query = SnapshotQuery(query_text="unicorno")
        results = await repo.find_by_label(query)
        assert results == []

    @pytest.mark.asyncio
    async def test_delete(self, mock_object_record: object) -> None:
        repo = MockObjectRepository()
        await repo.save(mock_object_record)
        await repo.delete(mock_object_record.id)
        result = await repo.get_by_id(mock_object_record.id)
        assert result is None
