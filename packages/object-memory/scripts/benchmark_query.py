"""Benchmark delle latenze di object-memory.

Misura le latenze delle operazioni principali:
- Elaborazione frame WebSocket (detection → labeling → save)
- Query REST per etichetta testuale
- Lista oggetti

Uso:
    python scripts/benchmark_query.py --frames 20
    python scripts/benchmark_query.py --frames 50 --warmup 5 --output results.csv
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import csv
import json
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(description="Benchmark latenze object-memory")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--frames", type=int, default=20, help="Frame da inviare (default: 20)")
    parser.add_argument("--warmup", type=int, default=3, help="Frame di warmup (default: 3)")
    parser.add_argument("--output", type=str, default="", help="File CSV di output")
    parser.add_argument("--image", type=str, default="", help="Immagine JPEG da usare (default: sintetica)")
    return parser.parse_args()


def make_synthetic_jpeg(width: int = 640, height: int = 480) -> bytes:
    """Genera un'immagine JPEG sintetica per i benchmark.

    Args:
        width: Larghezza in pixel.
        height: Altezza in pixel.

    Returns:
        Bytes JPEG.
    """
    import cv2
    import numpy as np

    frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    _, jpeg_bytes = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return jpeg_bytes.tobytes()


async def benchmark_frames(
    uri: str,
    image_b64: str,
    n_frames: int,
    warmup: int,
) -> list[float]:
    """Invia frame al WebSocket e misura le latenze di risposta.

    Args:
        uri: URI WebSocket del server.
        image_b64: Immagine JPEG codificata in base64.
        n_frames: Numero di frame da inviare dopo il warmup.
        warmup: Frame di warmup (latenze ignorate).

    Returns:
        Lista di latenze in millisecondi.
    """
    import websockets

    latencies: list[float] = []
    message = json.dumps({"type": "frame", "image": image_b64})

    async with websockets.connect(uri) as ws:
        for i in range(warmup + n_frames):
            t0 = time.perf_counter()
            await ws.send(message)
            await asyncio.wait_for(ws.recv(), timeout=10.0)
            elapsed_ms = (time.perf_counter() - t0) * 1000

            if i >= warmup:
                latencies.append(elapsed_ms)
                print(f"  frame {i - warmup + 1:3d}/{n_frames}: {elapsed_ms:.1f} ms")

    return latencies


async def benchmark_query(base_url: str, n_queries: int = 10) -> list[float]:
    """Misura le latenze delle query REST POST /api/query.

    Args:
        base_url: URL base del server.
        n_queries: Numero di query da eseguire.

    Returns:
        Lista di latenze in millisecondi.
    """
    import httpx

    latencies: list[float] = []
    payload = {"query": "oggetto", "language": "it", "max_results": 3}

    async with httpx.AsyncClient() as client:
        for i in range(n_queries):
            t0 = time.perf_counter()
            await client.post(f"{base_url}/api/query", json=payload)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            latencies.append(elapsed_ms)

    return latencies


def print_stats(label: str, values: list[float]) -> None:
    """Stampa statistiche descrittive per una lista di valori.

    Args:
        label: Nome della metrica.
        values: Lista di valori numerici.
    """
    if not values:
        return
    import statistics

    print(f"\n{label}:")
    print(f"  n       = {len(values)}")
    print(f"  mean    = {statistics.mean(values):.1f} ms")
    print(f"  median  = {statistics.median(values):.1f} ms")
    print(f"  stdev   = {statistics.stdev(values):.1f} ms" if len(values) > 1 else "  stdev   = N/A")
    print(f"  min     = {min(values):.1f} ms")
    print(f"  max     = {max(values):.1f} ms")


async def main(args: argparse.Namespace) -> None:
    """Entry point principale del benchmark.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    base_url = f"http://{args.host}:{args.port}"
    ws_uri = f"ws://{args.host}:{args.port}/ws"

    # Prepara immagine
    if args.image:
        image_bytes = Path(args.image).read_bytes()
    else:
        print("Generando immagine sintetica 640x480...")
        image_bytes = make_synthetic_jpeg()
    image_b64 = base64.b64encode(image_bytes).decode()

    print(f"\n{'='*60}")
    print(f"Benchmark object-memory @ {base_url}")
    print(f"Frames: {args.frames} (+ {args.warmup} warmup)")
    print(f"{'='*60}")

    # Benchmark frame WebSocket
    print(f"\n[1/2] Frame WebSocket ({args.frames} frames, {args.warmup} warmup):")
    try:
        frame_latencies = await benchmark_frames(ws_uri, image_b64, args.frames, args.warmup)
        print_stats("Frame WebSocket latency", frame_latencies)
    except Exception as exc:
        print(f"  ERRORE: {exc}", file=sys.stderr)
        frame_latencies = []

    # Benchmark query REST
    print(f"\n[2/2] REST Query POST /api/query (10 queries):")
    try:
        query_latencies = await benchmark_query(base_url, n_queries=10)
        print_stats("REST Query latency", query_latencies)
    except Exception as exc:
        print(f"  ERRORE: {exc}", file=sys.stderr)
        query_latencies = []

    # Salva CSV
    if args.output and (frame_latencies or query_latencies):
        with open(args.output, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "value_ms"])
            for v in frame_latencies:
                writer.writerow(["frame_ws", f"{v:.2f}"])
            for v in query_latencies:
                writer.writerow(["rest_query", f"{v:.2f}"])
        print(f"\nRisultati salvati in {args.output}")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))
