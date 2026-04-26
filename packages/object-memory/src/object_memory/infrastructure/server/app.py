"""FastAPI app factory per il server object-memory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from object_memory.infrastructure.config.settings import AppSettings
from object_memory.infrastructure.container import ObjectMemoryContainer
from object_memory.infrastructure.server.health import router as health_router
from object_memory.infrastructure.server.query_handler import router as query_router
from object_memory.infrastructure.server.websocket_handler import router as ws_router

logger = structlog.get_logger(__name__)


def create_app(settings: AppSettings, use_mocks: bool = False) -> FastAPI:
    """Crea e configura l'applicazione FastAPI.

    Args:
        settings: Configurazione dell'applicazione.
        use_mocks: Se True, usa adapter mock (senza GPU/DB).

    Returns:
        Applicazione FastAPI configurata.
    """
    container = ObjectMemoryContainer(settings=settings, use_mocks=use_mocks)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Gestisce il ciclo di vita dell'applicazione."""
        logger.info("server.starting", host=settings.server.host, port=settings.server.port)
        yield
        logger.info("server.shutting_down")
        if container._frame_source is not None:
            container._frame_source.release()

    app = FastAPI(
        title="object-memory",
        description="Memoria visiva degli oggetti per Meta Quest 3",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.container = container
    app.state.settings = settings

    app.include_router(health_router)
    app.include_router(ws_router)
    app.include_router(query_router)

    return app


__all__ = ["create_app"]
