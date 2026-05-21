"""Entry point del sistema vision-caption.

Avvia il server WebSocket caricando la configurazione da config.yaml,
inizializzando il DI container e lanciando Uvicorn.

Uso:
    python -m vision_caption
    python -m vision_caption --config /path/to/config.yaml --host 0.0.0.0 --port 8765
"""

from __future__ import annotations

import argparse
import sys

import structlog
import uvicorn

from vision_caption.infrastructure.config.settings import AppSettings, load_settings
from vision_commons.infrastructure.logging.setup import configure_logging
from vision_caption.infrastructure.server.app import create_app

logger = structlog.get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parsa gli argomenti da riga di comando.

    Returns:
        Namespace con i parametri parsati.
    """
    parser = argparse.ArgumentParser(
        prog="vision-caption",
        description="Sistema di audio-descrizione ambientale in tempo reale",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Percorso al file di configurazione YAML (default: config.yaml)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host su cui ascoltare (sovrascrive config.yaml)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Porta su cui ascoltare (sovrascrive config.yaml)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=None,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Livello di log (sovrascrive config.yaml)",
    )
    return parser.parse_args()


def main() -> None:
    """Punto di ingresso principale dell'applicazione.

    Carica la configurazione, configura il logging, crea la FastAPI app
    e avvia Uvicorn.
    """
    args = parse_args()

    # Carica settings da YAML
    settings: AppSettings = load_settings(config_path=args.config)

    # Applica override da CLI
    if args.host is not None:
        settings.server.host = args.host
    if args.port is not None:
        settings.server.port = args.port
    if args.log_level is not None:
        settings.logging.level = args.log_level

    # Configura structlog
    configure_logging(level=settings.logging.level)

    logger.info(
        "vision-caption starting",
        host=settings.server.host,
        port=settings.server.port,
        vlm_model=settings.vlm.model_name,
        tts_model=settings.tts.model,
    )

    # Crea FastAPI app con il container iniettato
    app = create_app(settings=settings)

    try:
        uvicorn.run(
            app,
            host=settings.server.host,
            port=settings.server.port,
            log_level=settings.logging.level.lower(),
            access_log=False,  # Logging strutturato gestito da structlog
            ws_ping_interval=None,
            ws_ping_timeout=None,
        )
    except KeyboardInterrupt:
        logger.info("vision-caption stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
