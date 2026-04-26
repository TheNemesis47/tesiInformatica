"""Test per MockSnapshotStore."""

from __future__ import annotations

import pytest

from object_memory.adapters.snapshot_store.mock_store import MockSnapshotStore


class TestMockSnapshotStore:
    @pytest.mark.asyncio
    async def test_save_returns_mock_path(self) -> None:
        store = MockSnapshotStore()
        path = await store.save("obj-123", b"\xff\xd8\xff")
        assert path.startswith("mock://obj-123/")
        assert path.endswith(".jpg")

    @pytest.mark.asyncio
    async def test_save_and_load(self) -> None:
        store = MockSnapshotStore()
        data = b"\xff\xd8\xff\xe0test"
        path = await store.save("obj-abc", data)
        loaded = await store.load(path)
        assert loaded == data

    @pytest.mark.asyncio
    async def test_save_increments_counter(self) -> None:
        store = MockSnapshotStore()
        path1 = await store.save("obj-1", b"data1")
        path2 = await store.save("obj-1", b"data2")
        assert path1 != path2
        assert store.save_count == 2

    @pytest.mark.asyncio
    async def test_load_missing_raises_key_error(self) -> None:
        store = MockSnapshotStore()
        with pytest.raises(KeyError):
            await store.load("mock://nonexistent/1.jpg")

    @pytest.mark.asyncio
    async def test_delete_removes_entry(self) -> None:
        store = MockSnapshotStore()
        path = await store.save("obj-del", b"bytes")
        await store.delete(path)
        with pytest.raises(KeyError):
            await store.load(path)

    @pytest.mark.asyncio
    async def test_delete_nonexistent_is_noop(self) -> None:
        store = MockSnapshotStore()
        # Non deve sollevare eccezioni
        await store.delete("mock://does/not/exist.jpg")

    @pytest.mark.asyncio
    async def test_multiple_objects_isolated(self) -> None:
        store = MockSnapshotStore()
        path_a = await store.save("obj-a", b"bytes_a")
        path_b = await store.save("obj-b", b"bytes_b")
        assert await store.load(path_a) == b"bytes_a"
        assert await store.load(path_b) == b"bytes_b"
