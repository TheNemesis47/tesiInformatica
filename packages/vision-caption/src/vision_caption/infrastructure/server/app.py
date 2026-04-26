"""FastAPI app factory per il server vision-caption.

Crea e configura l'applicazione FastAPI con:
- Middleware CORS per connessioni da Meta Quest 3
- Endpoint WebSocket /ws per lo streaming
- Endpoint HTTP /health per health check
- Event handler per startup/shutdown
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vision_caption.infrastructure.config.settings import AppSettings
from vision_caption.infrastructure.container import ApplicationContainer
from vision_caption.infrastructure.server.health import router as health_router
from vision_caption.infrastructure.server.websocket_handler import router as ws_router

logger = structlog.get_logger(__name__)


def create_app(
    settings: AppSettings,
    use_mocks: bool = False,
) -> FastAPI:
    """Crea e configura l'applicazione FastAPI.

    Args:
        settings: Configurazione dell'applicazione.
        use_mocks: Se True, usa adapter mock (senza GPU) invece di quelli reali.
            Usato per test e sviluppo.

    Returns:
        Applicazione FastAPI configurata e pronta per Uvicorn.
    """
    container = ApplicationContainer(settings=settings, use_mocks=use_mocks)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Gestisce il ciclo di vita dell'applicazione.

        Args:
            app: Istanza FastAPI (non usata direttamente).

        Yields:
            None durante il runtime dell'applicazione.
        """
        logger.info(
            "server.starting",
            host=settings.server.host,
            port=settings.server.port,
        )
        # Pre-warming dei modelli AI potrebbe avvenire qui
        yield
        logger.info("server.shutting_down")
        # Cleanup: rilascia risorse hardware se necessario
        if container._frame_source is not None:
            container._frame_source.release()

    app = FastAPI(
        title="vision-caption",
        description="Audio-descrizione ambientale in tempo reale per utenti ciechi/ipovedenti",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url=None,
    )

    # CORS: permette connessioni da Meta Quest 3 e client di test locali
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrингere in produzione
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inietta il container nell'app state per accesso dai router
    app.state.container = container
    app.state.settings = settings

    # Registra i router
    app.include_router(health_router)
    app.include_router(ws_router)

    logger.info("server.app_created")
    return app


__all__ = ["create_app"]
