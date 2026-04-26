"""Middleware FastAPI per vision-caption.

Middleware per gestione centralizzata degli errori e logging delle richieste.
"""

from __future__ import annotations

import time

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware che logga ogni richiesta HTTP con la sua latenza.

    Non logga le richieste WebSocket upgrade (già gestite dall'handler).
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Processa la richiesta e logga il risultato.

        Args:
            request: Richiesta HTTP in arrivo.
            call_next: Callable per passare la richiesta al prossimo handler.

        Returns:
            Response HTTP dal prossimo handler.
        """
        # Skip WebSocket upgrade requests
        if request.headers.get("upgrade", "").lower() == "websocket":
            return await call_next(request)

        t0 = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - t0) * 1000

        logger.info(
            "http.request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response


__all__ = ["RequestLoggingMiddleware"]
