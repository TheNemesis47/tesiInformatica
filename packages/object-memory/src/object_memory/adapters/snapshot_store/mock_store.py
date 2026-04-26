"""Mock snapshot store in-memory per i test."""

from __future__ import annotations


class MockSnapshotStore:
    """Store in-memory per test senza filesystem.

    Attributes:
        _store: Dizionario path → bytes in memoria.
        save_count: Numero di chiamate a save().
        _counter: Contatore per generare percorsi univoci.
    """

    def __init__(self) -> None:
        """Inizializza lo store vuoto."""
        self._store: dict[str, bytes] = {}
        self.save_count: int = 0
        self._counter: int = 0

    async def save(self, object_id: str, image_bytes: bytes) -> str:
        """Salva i bytes in memoria e restituisce un percorso mock."""
        self._counter += 1
        path = f"mock://{object_id}/{self._counter}.jpg"
        self._store[path] = image_bytes
        self.save_count += 1
        return path

    async def load(self, snapshot_path: str) -> bytes:
        """Carica i bytes dal percorso mock."""
        if snapshot_path not in self._store:
            raise KeyError(f"Snapshot not found: {snapshot_path}")
        return self._store[snapshot_path]

    async def delete(self, snapshot_path: str) -> None:
        """Elimina i bytes dal mock store."""
        self._store.pop(snapshot_path, None)


__all__ = ["MockSnapshotStore"]
