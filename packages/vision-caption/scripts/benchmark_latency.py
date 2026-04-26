"""Benchmark della latenza per ogni componente della pipeline.

Misura e stampa la distribuzione delle latenze (media, mediana, p95, p99)
per: scene detection (SSIM + RF-DETR), VLM (Gemma), TTS (Chatterbox).

Uso:
    python scripts/benchmark_latency.py --frames 50 --warmup 5
"""

from __future__ import annotations

import argparse
import asyncio
import statistics
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(description="Benchmark latenza pipeline vision-caption")
    parser.add_argument("--frames", type=int, default=30, help="Numero di frame da testare")
    parser.add_argument("--warmup", type=int, default=3, help="Frame di warmup (non conteggiati)")
    parser.add_argument("--image", type=str, default=None, help="Immagine JPEG di test")
    parser.add_argument("--config", type=str, default="config.yaml", help="File di configurazione")
    parser.add_argument("--output", type=str, default=None, help="File CSV per i risultati")
    return parser.parse_args()


def percentile(data: list[float], p: float) -> float:
    """Calcola il percentile p della lista data.

    Args:
        data: Lista di valori.
        p: Percentile [0, 100].

    Returns:
        Valore al percentile p.
    """
    sorted_data = sorted(data)
    idx = int(len(sorted_data) * p / 100)
    return sorted_data[min(idx, len(sorted_data) - 1)]


def print_stats(name: str, latencies_ms: list[float]) -> None:
    """Stampa le statistiche di latenza per un componente.

    Args:
        name: Nome del componente.
        latencies_ms: Lista di latenze in millisecondi.
    """
    if not latencies_ms:
        print(f"  {name}: nessun dato")
        return

    print(f"\n  {name}:")
    print(f"    n     = {len(latencies_ms)}")
    print(f"    mean  = {statistics.mean(latencies_ms):.1f} ms")
    print(f"    median= {statistics.median(latencies_ms):.1f} ms")
    print(f"    stdev = {statistics.stdev(latencies_ms):.1f} ms" if len(latencies_ms) > 1 else "    stdev = N/A")
    print(f"    min   = {min(latencies_ms):.1f} ms")
    print(f"    p95   = {percentile(latencies_ms, 95):.1f} ms")
    print(f"    p99   = {percentile(latencies_ms, 99):.1f} ms")
    print(f"    max   = {max(latencies_ms):.1f} ms")


async def run_benchmark(args: argparse.Namespace) -> None:
    """Esegue il benchmark della pipeline.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    # TODO: implementare il benchmark completo
    # 1. Carica config da args.config
    # 2. Crea container con adapter reali
    # 3. Carica immagine di test (da args.image o genera sintetica)
    # 4. Loop warmup + benchmark:
    #    - Misura SSIM latency
    #    - Misura RFDETR latency
    #    - Misura VLM latency
    #    - Misura TTS latency
    # 5. Stampa statistiche per ogni componente
    # 6. Se args.output, salva CSV

    print("=== vision-caption Latency Benchmark ===")
    print(f"Frames: {args.frames} (+{args.warmup} warmup)")
    print("NOTE: benchmark non ancora implementato — richiede adapter funzionanti")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_benchmark(args))
