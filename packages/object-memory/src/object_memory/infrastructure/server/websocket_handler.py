"""WebSocket handler per la ricezione dei frame da Meta Quest 3.

Riceve frame JPEG dal visore, li passa alla ObjectMemoryPipeline e
invia un ACK con il numero di oggetti aggiornati.

Protocollo client → server (JSON):
    {"type": "frame", "image": "<base64 JPEG>"}

Protocollo server → client (JSON):
    {"type": "ack", "updated": 2}      ← N oggetti aggiornati
    {"type": "ack", "updated": 0}      ← scena invariata, nessun aggiornamento
    {"type": "error", "message": "..."}
"""

from __future__ import annotations

import base64
import json

import structlog
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from object_memory.shared.errors import ObjectMemoryError
from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, request: Request) -> None:
    """Endpoint WebSocket per la ricezione di frame dal Meta Quest 3.

    Args:
        websocket: Connessione WebSocket.
        request: Request HTTP di upgrade.
    """
    await websocket.accept()
    client_host = websocket.client.host if websocket.client else "unknown"
    logger.info("websocket.client_connected", client=client_host)

    container = request.app.state.container
    pipeline = container.create_pipeline()

    try:
        while True:
            # TODO: implementare il loop
            # 1. raw = await websocket.receive_text()
            # 2. message = json.loads(raw)
            # 3. frame = _deserialize_frame(message)
            # 4. updated_count = await pipeline.process(frame)
            # 5. await websocket.send_text(json.dumps({"type": "ack", "updated": updated_count}))
            raise NotImplementedError

    except WebSocketDisconnect:
        logger.info("websocket.client_disconnected", client=client_host)
    except ObjectMemoryError as exc:
        logger.error("websocket.pipeline_error", error=str(exc))
        await _send_error(websocket, str(exc))


def _deserialize_frame(message: dict[str, object]) -> FrameData:
    """Deserializza un messaggio JSON in FrameData.

    Args:
        message: Dizionario con i campi del messaggio.

    Returns:
        FrameData con i bytes dell'immagine.
    """
    # TODO: implementare
    raise NotImplementedError


async def _send_error(websocket: WebSocket, message: str) -> None:
    """Invia un messaggio di errore JSON al client."""
    try:
        await websocket.send_text(json.dumps({"type": "error", "message": message}))
    except Exception:
        pass


__all__ = ["router"]
