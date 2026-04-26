"""Script per interrogare il catalogo degli oggetti memorizzati.

Invia una query testuale al server object-memory e stampa i risultati
con etichette e timestamp dell'ultimo avvistamento.

Uso:
    python scripts/query_objects.py --query "maglia rossa"
    python scripts/query_objects.py --list
    python scripts/query_objects.py --query "chiavi" --max-results 5
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando."""
    parser = argparse.ArgumentParser(description="Query del catalogo oggetti")
    parser.add_argument("--host", default="localhost", help="Host del server (default: localhost)")
    parser.add_argument("--port", type=int, default=8766, help="Porta del server (default: 8766)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", "-q", type=str, help="Testo da cercare (es. 'maglia rossa')")
    group.add_argument("--list", "-l", action="store_true", help="Lista tutti gli oggetti")
    parser.add_argument(
        "--max-results",
        type=int,
        default=3,
        help="Numero massimo di risultati per la query (default: 3)",
    )
    parser.add_argument(
        "--language",
        default="it",
        help="Lingua della query ISO 639-1 (default: it)",
    )
    return parser.parse_args()


async def list_objects(base_url: str) -> None:
    """Stampa la lista di tutti gli oggetti nel catalogo.

    Args:
        base_url: URL base del server (es. http://localhost:8766).
    """
    import httpx

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/api/objects")
        response.raise_for_status()
        objects = response.json()

    if not objects:
        print("Nessun oggetto nel catalogo.")
        return

    print(f"{'ID':36}  {'Etichetta':30}  {'Ultimo avv.':20}  {'Rilevm.'}")
    print("-" * 100)
    for obj in objects:
        last_seen = datetime.fromtimestamp(obj["last_seen_at"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{obj['id']:36}  {obj['label']:30}  {last_seen:20}  {obj['detection_count']}")


async def search_object(base_url: str, query: str, max_results: int, language: str) -> None:
    """Cerca un oggetto per etichetta testuale e stampa i risultati.

    Args:
        base_url: URL base del server.
        query: Testo da cercare.
        max_results: Numero massimo di risultati.
        language: Lingua della query.
    """
    import httpx

    payload = {"query": query, "language": language, "max_results": max_results}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/api/query", json=payload)
        response.raise_for_status()
        results = response.json()

    if not results:
        print(f"Nessun oggetto trovato per '{query}'.")
        return

    print(f"Trovati {len(results)} risultati per '{query}':\n")
    for i, result in enumerate(results, 1):
        last_seen = datetime.fromtimestamp(result["last_seen_at"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {i}. {result['label']}")
        print(f"     ID: {result['id']}")
        print(f"     Ultimo avvistamento: {last_seen}")
        print(f"     Risposta: {result['response_text']}")
        print()


async def main(args: argparse.Namespace) -> None:
    """Entry point principale.

    Args:
        args: Argomenti parsati.
    """
    base_url = f"http://{args.host}:{args.port}"

    try:
        if args.list:
            await list_objects(base_url)
        else:
            await search_object(base_url, args.query, args.max_results, args.language)
    except Exception as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))
