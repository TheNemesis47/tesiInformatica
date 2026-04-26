"""Mock repository in-memory per i test."""

from __future__ import annotations

from object_memory.core.domain.object_record import ObjectRecord
from object_memory.core.domain.snapshot import SnapshotQuery


class MockObjectRepository:
    """Repository in-memory per test senza database.

    Attributes:
        _store: Dizionario id → ObjectRecord in memoria.
        save_count: Numero di chiamate a save().
    """

    def __init__(self) -> None:
        """Inizializza il repository vuoto."""
        self._store: dict[str, ObjectRecord] = {}
        self.save_count: int = 0

    async def save(self, record: ObjectRecord) -> None:
        """Salva o aggiorna un record in memoria."""
        self._store[record.id] = record
        self.save_count += 1

    async def find_by_label(self, query: SnapshotQuery) -> list[ObjectRecord]:
        """Cerca per corrispondenza parziale del testo etichetta."""
        q = query.query_text.lower()
        matches = [r for r in self._store.values() if q in r.label.text.lower()]
        return sorted(matches, key=lambda r: r.last_seen_at, reverse=True)[: query.max_results]

    async def get_by_id(self, object_id: str) -> ObjectRecord | None:
        """Recupera un record per ID."""
        return self._store.get(object_id)

    async def get_all(self) -> list[ObjectRecord]:
        """Recupera tutti i record."""
        return sorted(self._store.values(), key=lambda r: r.last_seen_at, reverse=True)

    async def delete(self, object_id: str) -> None:
        """Elimina un record."""
        self._store.pop(object_id, None)


__all__ = ["MockObjectRepository"]
