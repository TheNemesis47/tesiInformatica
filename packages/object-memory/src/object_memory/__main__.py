"""Entry point di object-memory."""

from __future__ import annotations

import argparse
import sys

import structlog
import uvicorn

from object_memory.infrastructure.config.settings import AppSettings, load_settings
from object_memory.infrastructure.server.app import create_app
from vision_commons.infrastructure.logging.setup import configure_logging

logger = structlog.get_logger(__name__)


def main() -> None:
    """Avvia il server object-memory."""
    parser = argparse.ArgumentParser(description="object-memory server")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--host", default=None)
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--log-level", default=None)
    args = parser.parse_args()

    settings: AppSettings = load_settings(config_path=args.config)
    if args.host:
        settings.server.host = args.host
    if args.port:
        settings.server.port = args.port
    if args.log_level:
        settings.logging.level = args.log_level

    configure_logging(level=settings.logging.level)
    logger.info("object-memory starting", host=settings.server.host, port=settings.server.port)

    app = create_app(settings=settings)
    try:
        uvicorn.run(app, host=settings.server.host, port=settings.server.port, access_log=False)
    except KeyboardInterrupt:
        logger.info("object-memory stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
