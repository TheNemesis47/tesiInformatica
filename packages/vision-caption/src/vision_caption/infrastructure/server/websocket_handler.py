"""WebSocket handler per lo streaming di frame e audio.

Gestisce la connessione WebSocket con il client (Meta Quest 3 o script di test):
- Riceve messaggi JSON con frame JPEG encoded in base64
- Passa il frame alla CaptionPipeline
- Invia il risultato audio come messaggio binario

Protocollo messaggi client → server:
    {
        "type": "frame",
        "image": "<base64-encoded JPEG>",
        "mode": "AUTO" | "POINTING",
        "pointing_x": 0.5,   # solo in modalità POINTING [0, 1]
        "pointing_y": 0.5,   # solo in modalità POINTING [0, 1]
        "crop_size": 320      # solo in modalità POINTING
    }

Protocollo messaggi server → client:
    Messaggio binario con i bytes audio (WAV o Opus)
    oppure JSON per errori:
    {"type": "error", "message": "..."}
"""

from __future__ import annotations

import base64
import json

import structlog
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from vision_commons.domain.frame import CaptureMode, FrameData, FrameMetadata
from vision_caption.shared.errors import VisionCaptionError

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Endpoint WebSocket principale per lo streaming audio-descrizione.

    Accetta connessioni WebSocket, riceve frame JPEG e invia audio sintetizzato.
    Gestisce un solo client alla volta (come da configurazione max_connections=1).

    Args:
        websocket: Connessione WebSocket con il client.
    """
    await websocket.accept()
    client_host = websocket.client.host if websocket.client else "unknown"
    logger.info("websocket.client_connected", client=client_host)

    container = websocket.app.state.container
    pipeline = container.create_pipeline()

    try:
        while True:
            raw_message = await websocket.receive_text()
            message = json.loads(raw_message)
            frame = _deserialize_frame(message)
            result = await pipeline.process(frame)
            if result is not None:
                await websocket.send_bytes(result.audio_bytes)

    except WebSocketDisconnect:
        logger.info("websocket.client_disconnected", client=client_host)
    except VisionCaptionError as exc:
        logger.error("websocket.pipeline_error", error=str(exc), client=client_host)
        await _send_error(websocket, str(exc))
    except Exception as exc:
        logger.exception("websocket.unexpected_error", client=client_host)
        await _send_error(websocket, "Internal server error")


def _deserialize_frame(message: dict[str, object]) -> FrameData:
    """Deserializza un messaggio JSON in un FrameData.

    Args:
        message: Dizionario con i campi del messaggio ricevuto dal client.

    Returns:
        FrameData con i bytes dell'immagine e i metadati.

    Raises:
        VisionCaptionError: Se il messaggio è malformato o mancano campi obbligatori.
    """
    if "image" not in message:
        raise VisionCaptionError("Missing 'image' field in message")
    if "mode" not in message:
        raise VisionCaptionError("Missing 'mode' field in message")

    try:
        image_bytes = base64.b64decode(str(message["image"]))
    except Exception as e:
        raise VisionCaptionError("Invalid base64 image encoding") from e

    mode_str = str(message["mode"]).upper()
    try:
        mode = CaptureMode[mode_str]
    except KeyError:
        mode = CaptureMode.AUTO

    pointing_coords = None
    if mode == CaptureMode.POINTING:
        if "pointing_x" in message and "pointing_y" in message:
            pointing_coords = (float(message["pointing_x"]), float(message["pointing_y"]))

    metadata = FrameMetadata(
        mode=mode,
        pointing_coords=pointing_coords,
    )

    return FrameData(image_bytes=image_bytes, metadata=metadata)


async def _send_error(websocket: WebSocket, message: str) -> None:
    """Invia un messaggio di errore JSON al client.

    Args:
        websocket: Connessione WebSocket attiva.
        message: Testo del messaggio di errore.
    """
    try:
        await websocket.send_text(json.dumps({"type": "error", "message": message}))
    except Exception:
        pass  # Client già disconnesso


__all__ = ["router"]
