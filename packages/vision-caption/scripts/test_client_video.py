"""Client di test per vision-caption con file video pre-registrato.

Legge frame da un file video e li invia al server WebSocket come se
fossero frame live, per test riproducibili senza webcam.

Uso:
    python scripts/test_client_video.py --video /path/to/video.mp4
    python scripts/test_client_video.py --video test.mp4 --fps 2
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
        description="Client di test vision-caption con file video"
    )
    parser.add_argument("--video", required=True, help="Percorso al file video")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--fps", type=float, default=2.0, help="Frame al secondo da inviare")
    parser.add_argument("--quality", type=int, default=75, help="Qualità JPEG [0-100]")
    return parser.parse_args()


async def run_client(args: argparse.Namespace) -> None:
    """Avvia il client WebSocket con il file video.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    import cv2
    import websockets

    uri = f"ws://{args.host}:{args.port}/ws"
    interval_sec = 1.0 / args.fps

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video file: {args.video}", file=sys.stderr)
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video: {args.video} ({total_frames} frames @ {video_fps:.1f} FPS)")
    print(f"Sending at {args.fps} FPS → interval {interval_sec*1000:.0f}ms")

    try:
        async with websockets.connect(uri) as ws:
            print(f"Connected to {uri}")
            frame_count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"\nVideo ended after {frame_count} frames")
                    break

                encode_params = [cv2.IMWRITE_JPEG_QUALITY, args.quality]
                _, jpeg_bytes = cv2.imencode(".jpg", frame, encode_params)
                image_b64 = base64.b64encode(jpeg_bytes.tobytes()).decode("utf-8")

                message = json.dumps({
                    "type": "frame",
                    "image": image_b64,
                    "mode": "AUTO",
                })
                await ws.send(message)
                frame_count += 1
                print(f"\rFrame {frame_count}/{total_frames}", end="", flush=True)

                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=0.05)
                    if isinstance(response, bytes) and len(response) > 0:
                        print(f"\n→ Audio received: {len(response)} bytes")
                except asyncio.TimeoutError:
                    pass

                await asyncio.sleep(interval_sec)

    except KeyboardInterrupt:
        print("\nClient stopped by user")
    finally:
        cap.release()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_client(args))
