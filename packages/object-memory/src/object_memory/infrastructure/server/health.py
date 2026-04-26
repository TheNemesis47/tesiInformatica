"""Health check endpoint per object-memory."""

from __future__ import annotations

import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])

_start_time: float = time.time()


class HealthResponse(BaseModel):
    """Risposta dell'endpoint health check."""

    status: str
    uptime_sec: float
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Verifica lo stato del server."""
    from object_memory import __version__
    return HealthResponse(
        status="ok",
        uptime_sec=round(time.time() - _start_time, 2),
        version=__version__,
    )


__all__ = ["router"]
