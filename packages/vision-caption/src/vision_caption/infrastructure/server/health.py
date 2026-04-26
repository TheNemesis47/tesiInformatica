"""Endpoint HTTP /health per health check del server.

Usato da deploy (Docker, SLURM) e da sistemi di monitoraggio per
verificare che il server sia operativo.
"""

from __future__ import annotations

import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Risposta dell'endpoint di health check.

    Attributes:
        status: Stato del server ("ok" o "degraded").
        uptime_sec: Secondi dall'avvio del server.
        version: Versione dell'applicazione.
    """

    status: str
    uptime_sec: float
    version: str


_start_time: float = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Verifica lo stato del server.

    Returns:
        HealthResponse con stato e uptime.
    """
    from vision_caption import __version__

    return HealthResponse(
        status="ok",
        uptime_sec=round(time.time() - _start_time, 2),
        version=__version__,
    )


__all__ = ["router"]
