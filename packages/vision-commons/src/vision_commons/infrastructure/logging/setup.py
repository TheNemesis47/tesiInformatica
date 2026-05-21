"""Configurazione di structlog per logging strutturato in JSON.

Imposta structlog con processori appropriati per l'ambiente:
- Sviluppo: output colorato e leggibile su console
- Produzione/SLURM: output JSON per aggregatori di log
"""

from __future__ import annotations

import logging
import sys

import structlog


def configure_logging(level: str = "INFO", json_output: bool = False) -> None:
    """Configura structlog per l'intera applicazione.

    Deve essere chiamato una sola volta all'avvio, prima di qualsiasi
    utilizzo del logger. Configura sia structlog sia il logging stdlib
    per garantire la compatibilità con le librerie di terze parti.

    Args:
        level: Livello di log (DEBUG, INFO, WARNING, ERROR).
            Case-insensitive.
        json_output: Se True, produce JSON compatto (per produzione/SLURM).
            Se False, produce output colorato e leggibile (per sviluppo).
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configura stdlib logging per catturare i log delle librerie esterne
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_output:
        # Produzione: JSON compatto
        processors: list[structlog.types.Processor] = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Sviluppo: output colorato con ConsoleRenderer
        processors = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=[structlog.stdlib.filter_by_level] + processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


__all__ = ["configure_logging"]
