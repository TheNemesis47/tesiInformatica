"""Servizio di query per la ricerca degli oggetti memorizzati.

Risponde alle domande dell'utente tipo "dove si trova la maglia rossa?"
cercando nel DB per similarità testuale e restituendo lo snapshot
aggiornato dell'oggetto.
"""

from __future__ import annotations

import structlog

from object_memory.core.domain.snapshot import ObjectSnapshot, SnapshotQuery
from object_memory.core.ports.object_repository import ObjectRepositoryPort
from object_memory.core.ports.snapshot_store import SnapshotStorePort

logger = structlog.get_logger(__name__)


class ObjectQueryService:
    """Servizio per la ricerca di oggetti nel catalogo.

    Gestisce le query dell'utente (testo in ingresso) e le traduce
    in ricerche nel DB, restituendo gli snapshot con il testo di risposta.

    Attributes:
        _repository: Repository degli ObjectRecord.
        _snapshot_store: Store per recuperare gli screenshot.
    """

    def __init__(
        self,
        repository: ObjectRepositoryPort,
        snapshot_store: SnapshotStorePort,
    ) -> None:
        """Inizializza il query service.

        Args:
            repository: Repository degli ObjectRecord.
            snapshot_store: Store per il recupero degli screenshot.
        """
        self._repository = repository
        self._snapshot_store = snapshot_store

    async def search(self, query: SnapshotQuery) -> list[ObjectSnapshot]:
        """Cerca oggetti che corrispondono alla query e restituisce gli snapshot.

        Args:
            query: Query dell'utente con testo e parametri di filtraggio.

        Returns:
            Lista di ObjectSnapshot (max query.max_results), ordinata per
            rilevanza. Lista vuota se nessun oggetto corrisponde.
        """
        # TODO: implementare
        # 1. records = await self._repository.find_by_label(query)
        # 2. if not records → return []
        # 3. results = []
        # 4. for record in records[:query.max_results]:
        #     a. snapshot_bytes = await self._snapshot_store.load(record.last_snapshot_path)
        #     b. response_text = _build_response_text(record, query.language)
        #     c. results.append(ObjectSnapshot(record=record, snapshot_bytes=snapshot_bytes,
        #                                       response_text=response_text))
        # 5. return results
        raise NotImplementedError

    async def get_all_objects(self) -> list[str]:
        """Restituisce le etichette di tutti gli oggetti nel catalogo.

        Usato per popolare l'interfaccia utente con la lista degli oggetti
        memorizzati.

        Returns:
            Lista di stringhe con le etichette degli oggetti, ordinata
            per ultimo avvistamento (più recente prima).
        """
        # TODO: implementare
        # records = await self._repository.get_all()
        # return [r.label.text for r in records]
        raise NotImplementedError


def _build_response_text(record: object, language: str) -> str:
    """Costruisce il testo di risposta per l'utente.

    Args:
        record: ObjectRecord dell'oggetto trovato.
        language: Lingua della risposta (ISO 639-1).

    Returns:
        Testo da sintetizzare vocalmente con la posizione dell'oggetto.
    """
    # TODO: implementare risposta localizzata
    # es. "La maglia rossa è stata vista 3 minuti fa
    #      sul lato sinistro dell'inquadratura."
    raise NotImplementedError


__all__ = ["ObjectQueryService"]
