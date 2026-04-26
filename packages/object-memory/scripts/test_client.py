"""Client di test per object-memory con webcam.

Apre la webcam, cattura frame a intervalli regolari e li invia al server
WebSocket di object-memory. Stampa il numero di oggetti aggiornati per frame.

Uso:
    python scripts/test_client.py
    python scripts/test_client.py --host localhost --port 8766
    python scripts/test_client.py --interval 1000 --quality 80
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
        description="Client di test object-memory con webcam"
    )
    parser.add_argument("--host", default="localhost", help="Host del server (default: localhost)")
    parser.add_argument("--port", type=int, default=8766, help="Porta del server (default: 8766)")
    parser.add_argument(
        "--interval",
        type=int,
        default=1000,
        help="Intervallo tra frame in ms (default: 1000)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=80,
        help="Qualità JPEG [0-100] (default: 80)",
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
        default=1280,
        help="Larghezza frame (default: 1280)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Altezza frame (default: 720)",
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
            print("Connected to server. Streaming frames... (Ctrl+C to stop)\n")
            frame_count = 0
            total_updated = 0
            start_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame", file=sys.stderr)
                    break

                encode_params = [cv2.IMWRITE_JPEG_QUALITY, args.quality]
                _, jpeg_bytes = cv2.imencode(".jpg", frame, encode_params)
                image_b64 = base64.b64encode(jpeg_bytes.tobytes()).decode("utf-8")

                message = json.dumps({
                    "type": "frame",
                    "image": image_b64,
                })
                await ws.send(message)
                frame_count += 1

                try:
                    response_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
                    if isinstance(response_raw, str):
                        response = json.loads(response_raw)
                        if response.get("type") == "ack":
                            updated = response.get("updated", 0)
                            total_updated += updated
                            elapsed = time.time() - start_time
                            print(
                                f"[{elapsed:6.1f}s] frame={frame_count:4d}  "
                                f"updated={updated:2d}  total_objects={total_updated}"
                            )
                        elif response.get("type") == "error":
                            print(f"Server error: {response.get('message')}", file=sys.stderr)
                except asyncio.TimeoutError:
                    print(f"[frame {frame_count}] timeout waiting for ACK", file=sys.stderr)

                await asyncio.sleep(args.interval / 1000.0)

    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\nClient stopped. Sent {frame_count} frames in {elapsed:.1f}s.")
    finally:
        cap.release()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_client(args))
