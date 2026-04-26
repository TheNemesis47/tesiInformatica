"""Port per la persistenza degli oggetti nel database.

Definisce le operazioni CRUD sul catalogo degli oggetti memorizzati.
Implementato da SQLiteObjectRepository (adapters/repository).
"""

from __future__ import annotations

from typing import Protocol

from object_memory.core.domain.object_record import ObjectRecord
from object_memory.core.domain.snapshot import SnapshotQuery


class ObjectRepositoryPort(Protocol):
    """Interfaccia per la persistenza degli ObjectRecord.

    Astrae il database sottostante (SQLite in locale, potenzialmente
    PostgreSQL in produzione) permettendo lo swap senza modificare
    la pipeline.
    """

    async def save(self, record: ObjectRecord) -> None:
        """Persiste un nuovo ObjectRecord o aggiorna quello esistente.

        Se esiste già un record con lo stesso ``id``, lo sovrascrive.

        Args:
            record: Record da salvare o aggiornare.
        """
        ...

    async def find_by_label(self, query: SnapshotQuery) -> list[ObjectRecord]:
        """Cerca oggetti per similarità testuale dell'etichetta.

        Args:
            query: Query con il testo da cercare e parametri di filtraggio.

        Returns:
            Lista di ObjectRecord ordinata per rilevanza, al massimo
            ``query.max_results`` elementi.
        """
        ...

    async def get_by_id(self, object_id: str) -> ObjectRecord | None:
        """Recupera un oggetto tramite il suo ID univoco.

        Args:
            object_id: UUID dell'oggetto.

        Returns:
            ObjectRecord se trovato, None altrimenti.
        """
        ...

    async def get_all(self) -> list[ObjectRecord]:
        """Recupera tutti gli oggetti nel catalogo.

        Returns:
            Lista di tutti gli ObjectRecord, ordinata per last_seen_at desc.
        """
        ...

    async def delete(self, object_id: str) -> None:
        """Elimina un oggetto dal catalogo.

        Args:
            object_id: UUID dell'oggetto da eliminare.
        """
        ...


__all__ = ["ObjectRepositoryPort"]
