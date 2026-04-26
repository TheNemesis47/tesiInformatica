"""Test interattivo dei prompt Gemma via Ollama.

Permette di testare i prompt con immagini reali per valutare la qualità
delle caption prima di integrare il sistema completo.

Uso:
    python scripts/test_gemma_prompt.py --image /path/to/image.jpg
    python scripts/test_gemma_prompt.py --image img.jpg --mode pointing
    python scripts/test_gemma_prompt.py --image img.jpg --prompt "Descrivi i pericoli"
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import sys
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(description="Test interattivo prompt Gemma")
    parser.add_argument("--image", required=True, help="Percorso immagine JPEG/PNG")
    parser.add_argument(
        "--mode",
        choices=["auto", "pointing"],
        default="auto",
        help="Modalità caption (default: auto)",
    )
    parser.add_argument("--prompt", type=str, default=None, help="Prompt personalizzato")
    parser.add_argument("--model", type=str, default="gemma4:e4b", help="Modello Ollama")
    parser.add_argument("--repeat", type=int, default=1, help="Numero di ripetizioni")
    return parser.parse_args()


async def run_test(args: argparse.Namespace) -> None:
    """Esegue il test del prompt Gemma.

    Args:
        args: Argomenti parsati da riga di comando.
    """
    # TODO: implementare quando GemmaCaptionGenerator è funzionante
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"ERROR: Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    from vision_caption.adapters.captioning.prompts.prompt_templates import get_prompt
    from vision_caption.core.domain.frame import CaptureMode

    mode = CaptureMode.AUTO if args.mode == "auto" else CaptureMode.POINTING
    prompt = args.prompt or get_prompt(mode)

    print(f"=== Gemma Prompt Test ===")
    print(f"Image: {image_path}")
    print(f"Mode:  {mode.value}")
    print(f"Model: {args.model}")
    print(f"\nPrompt:\n{prompt}\n")
    print("NOTE: richiede GemmaCaptionGenerator implementato e Ollama running")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_test(args))
