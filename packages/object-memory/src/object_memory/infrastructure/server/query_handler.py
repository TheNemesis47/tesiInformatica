"""Endpoint REST per la ricerca degli oggetti memorizzati.

Fornisce le API HTTP per le query vocali/testuali dell'utente:
- GET /objects — lista tutti gli oggetti nel catalogo
- POST /query — cerca un oggetto per etichetta testuale
- GET /objects/{id}/snapshot — recupera lo screenshot di un oggetto
"""

from __future__ import annotations

import base64

import structlog
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from object_memory.core.domain.snapshot import SnapshotQuery

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api", tags=["query"])


class QueryRequest(BaseModel):
    """Corpo della richiesta di ricerca.

    Attributes:
        query: Testo da cercare (es. "maglia rossa").
        language: Lingua della query (ISO 639-1).
        max_results: Numero massimo di risultati.
    """

    query: str
    language: str = "it"
    max_results: int = 3


class ObjectSummary(BaseModel):
    """Sommario di un oggetto per la lista.

    Attributes:
        id: UUID dell'oggetto.
        label: Etichetta testuale.
        last_seen_at: Timestamp Unix dell'ultimo avvistamento.
        detection_count: Numero totale di rilevamenti.
    """

    id: str
    label: str
    last_seen_at: float
    detection_count: int


class QueryResult(BaseModel):
    """Risultato di una query di ricerca.

    Attributes:
        id: UUID dell'oggetto trovato.
        label: Etichetta dell'oggetto.
        snapshot_b64: Screenshot JPEG codificato in base64.
        response_text: Testo di risposta per la sintesi vocale.
        last_seen_at: Timestamp Unix dell'ultimo avvistamento.
    """

    id: str
    label: str
    snapshot_b64: str
    response_text: str
    last_seen_at: float


@router.get("/objects", response_model=list[ObjectSummary])
async def list_objects(request: Request) -> list[ObjectSummary]:
    """Restituisce la lista di tutti gli oggetti nel catalogo.

    Args:
        request: Request HTTP (per accedere all'app state).

    Returns:
        Lista di ObjectSummary ordinata per ultimo avvistamento.
    """
    # TODO: implementare
    # query_service = request.app.state.container.create_query_service()
    # records = await query_service._repository.get_all()
    # return [ObjectSummary(id=r.id, label=r.label.text,
    #          last_seen_at=r.last_seen_at, detection_count=r.detection_count)
    #         for r in records]
    raise NotImplementedError


@router.post("/query", response_model=list[QueryResult])
async def search_object(body: QueryRequest, request: Request) -> list[QueryResult]:
    """Cerca oggetti per etichetta testuale.

    Args:
        body: Query con il testo da cercare.
        request: Request HTTP (per accedere all'app state).

    Returns:
        Lista di QueryResult con screenshot e testo di risposta.
    """
    # TODO: implementare
    # query_service = request.app.state.container.create_query_service()
    # query = SnapshotQuery(query_text=body.query, language=body.language,
    #                       max_results=body.max_results)
    # snapshots = await query_service.search(query)
    # return [QueryResult(id=s.record.id, label=s.record.label.text,
    #          snapshot_b64=base64.b64encode(s.snapshot_bytes).decode(),
    #          response_text=s.response_text,
    #          last_seen_at=s.record.last_seen_at) for s in snapshots]
    raise NotImplementedError


__all__ = ["router"]
