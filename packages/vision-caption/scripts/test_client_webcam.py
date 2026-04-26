"""Client di test per vision-caption con webcam Logitech Brio 4K.

Apre la webcam, cattura frame a intervalli regolari, li invia al server
WebSocket e riproduce l'audio ricevuto in risposta.

Uso:
    python scripts/test_client_webcam.py
    python scripts/test_client_webcam.py --host localhost --port 8765
    python scripts/test_client_webcam.py --interval 500 --quality 75
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import sys
import time


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(
        description="Client di test vision-caption con webcam Brio 4K"
    )
    parser.add_argument("--host", default="localhost", help="Host del server (default: localhost)")
    parser.add_argument("--port", type=int, default=8765, help="Porta del server (default: 8765)")
    parser.add_argument(
        "--interval",
        type=int,
        default=500,
        help="Intervallo tra frame in ms (default: 500)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=75,
        help="Qualità JPEG [0-100] (default: 75)",
    )
    parser.add_argument(
        "--device",
        type=int,
        default=0,
        help="ID dispositivo webcam (default: 0)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Larghezza frame webcam (default: 1920)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Altezza frame webcam (default: 1080)",
    )
    return parser.parse_args()


async def run_client(args: argparse.Namespace) -> None:
    """Avvia il client WebSocket con la webcam.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    import cv2
    import websockets

    uri = f"ws://{args.host}:{args.port}/ws"
    print(f"Connecting to {uri}...")

    cap = cv2.VideoCapture(args.device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    if not cap.isOpened():
        print(f"ERROR: Cannot open camera device {args.device}", file=sys.stderr)
        sys.exit(1)

    print(f"Camera opened: {args.width}x{args.height} @ device {args.device}")

    try:
        async with websockets.connect(uri) as ws:
            print("Connected to server")
            frame_count = 0
            start_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame", file=sys.stderr)
                    break

                # Comprimi in JPEG
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, args.quality]
                _, jpeg_bytes = cv2.imencode(".jpg", frame, encode_params)
                image_b64 = base64.b64encode(jpeg_bytes.tobytes()).decode("utf-8")

                # Invia al server
                message = json.dumps({
                    "type": "frame",
                    "image": image_b64,
                    "mode": "AUTO",
                })
                await ws.send(message)
                frame_count += 1

                # Ricevi risposta audio (non bloccante)
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=0.1)
                    if isinstance(response, bytes) and len(response) > 0:
                        elapsed = time.time() - start_time
                        print(f"[{elapsed:.1f}s] Frame {frame_count}: audio received ({len(response)} bytes)")
                        # TODO: riprodurre audio con sounddevice o pygame
                    elif isinstance(response, str):
                        msg = json.loads(response)
                        if msg.get("type") == "error":
                            print(f"Server error: {msg.get('message')}", file=sys.stderr)
                except asyncio.TimeoutError:
                    pass  # Nessuna risposta in questo ciclo

                await asyncio.sleep(args.interval / 1000.0)

    except KeyboardInterrupt:
        print("\nClient stopped by user")
    finally:
        cap.release()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_client(args))
