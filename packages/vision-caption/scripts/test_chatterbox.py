"""Test standalone di Chatterbox TTS.

Permette di testare la sintesi vocale Chatterbox isolatamente,
senza avviare il server completo.

Uso:
    python scripts/test_chatterbox.py --text "Buongiorno, ci sono gradini davanti a te."
    python scripts/test_chatterbox.py --text "Test" --output output.wav --device cpu
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(description="Test standalone Chatterbox TTS")
    parser.add_argument(
        "--text",
        type=str,
        default="Buongiorno. Ci sono tre gradini davanti a te. Attenzione.",
        help="Testo da sintetizzare",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.wav",
        help="File di output WAV (default: output.wav)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "cpu", "mps"],
        help="Device PyTorch (default: cuda)",
    )
    parser.add_argument(
        "--exaggeration",
        type=float,
        default=0.3,
        help="Espressività voce [0-1] (default: 0.3)",
    )
    parser.add_argument(
        "--cfg-weight",
        type=float,
        default=0.5,
        help="CFG weight [0-1] (default: 0.5)",
    )
    return parser.parse_args()


async def run_test(args: argparse.Namespace) -> None:
    """Esegue la sintesi TTS e salva il risultato su file.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    # TODO: implementare quando ChatterboxSynthesizer è funzionante
    print(f"=== Chatterbox TTS Test ===")
    print(f"Text:        {args.text!r}")
    print(f"Device:      {args.device}")
    print(f"Exaggeration:{args.exaggeration}")
    print(f"CFG weight:  {args.cfg_weight}")
    print(f"Output:      {args.output}")
    print("\nNOTE: richiede ChatterboxSynthesizer implementato e GPU disponibile")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_test(args))
