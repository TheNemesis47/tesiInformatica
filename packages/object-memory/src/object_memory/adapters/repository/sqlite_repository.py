"""Repository SQLite per gli ObjectRecord.

Usa aiosqlite per operazioni asincrone sul database. Lo schema viene
creato automaticamente al primo utilizzo (schema migrations semplici
adatte per un progetto di tesi).
"""

from __future__ import annotations

import json
from pathlib import Path

import structlog

from object_memory.core.domain.object_record import ObjectLabel, ObjectRecord, SpatialPosition
from object_memory.core.domain.snapshot import SnapshotQuery
from vision_commons.domain.detection import BoundingBox

logger = structlog.get_logger(__name__)

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS object_records (
    id TEXT PRIMARY KEY,
    label_text TEXT NOT NULL,
    label_language TEXT NOT NULL DEFAULT 'it',
    label_confidence REAL,
    label_assigned_at REAL NOT NULL,
    position_json TEXT NOT NULL,   -- JSON serializzato di SpatialPosition
    last_snapshot_path TEXT NOT NULL,
    first_seen_at REAL NOT NULL,
    last_seen_at REAL NOT NULL,
    detection_count INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_label_text ON object_records(label_text);
CREATE INDEX IF NOT EXISTS idx_last_seen_at ON object_records(last_seen_at DESC);
"""


class SQLiteObjectRepository:
    """Repository SQLite asincrono per gli ObjectRecord.

    Attributes:
        db_path: Percorso al file del database SQLite.
    """

    def __init__(self, db_path: Path | str = "data/object_memory.db") -> None:
        """Inizializza il repository SQLite.

        Args:
            db_path: Percorso al file SQLite. Viene creato se non esiste.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db: object | None = None  # aiosqlite.Connection

    async def _ensure_connected(self) -> None:
        """Apre la connessione e crea lo schema se necessario (lazy)."""
        # TODO: implementare
        # import aiosqlite
        # if self._db is None:
        #     self._db = await aiosqlite.connect(str(self.db_path))
        #     await self._db.executescript(_SCHEMA_SQL)
        #     await self._db.commit()
        raise NotImplementedError

    async def save(self, record: ObjectRecord) -> None:
        """Salva o aggiorna un ObjectRecord nel database."""
        # TODO: implementare con INSERT OR REPLACE
        raise NotImplementedError

    async def find_by_label(self, query: SnapshotQuery) -> list[ObjectRecord]:
        """Cerca oggetti per label con LIKE (full-text semplice)."""
        # TODO: implementare
        # SELECT * FROM object_records WHERE label_text LIKE '%query_text%'
        # ORDER BY last_seen_at DESC LIMIT max_results
        raise NotImplementedError

    async def get_by_id(self, object_id: str) -> ObjectRecord | None:
        """Recupera un ObjectRecord per ID."""
        # TODO: implementare
        raise NotImplementedError

    async def get_all(self) -> list[ObjectRecord]:
        """Recupera tutti gli ObjectRecord ordinati per last_seen_at desc."""
        # TODO: implementare
        raise NotImplementedError

    async def delete(self, object_id: str) -> None:
        """Elimina un ObjectRecord dal database."""
        # TODO: implementare
        raise NotImplementedError

    async def close(self) -> None:
        """Chiude la connessione al database."""
        # TODO: implementare
        raise NotImplementedError


__all__ = ["SQLiteObjectRepository"]
