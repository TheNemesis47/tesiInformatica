"""Misurazione della latenza per benchmark della pipeline.

Fornisce un context manager che misura il tempo di esecuzione di un blocco
di codice e lo logga con structlog in formato JSON-compatibile.

Supporta nesting per misurare sub-componenti della pipeline:
    async with LatencyTracker("pipeline") as total:
        async with LatencyTracker("pipeline.scene_detection"):
            ...
        async with LatencyTracker("pipeline.vlm"):
            ...
        async with LatencyTracker("pipeline.tts"):
            ...
    # total.elapsed_ms contiene la latenza end-to-end
"""

from __future__ import annotations

import time
from types import TracebackType

import structlog

logger = structlog.get_logger(__name__)


class LatencyTracker:
    """Context manager per la misurazione della latenza di un'operazione.

    Misura il tempo dall'entrata all'uscita del blocco ``with`` e logga
    il risultato con structlog. Può essere usato sia come context manager
    sincrono sia asincrono.

    Attributes:
        name: Nome dell'operazione misurata (usato come chiave nel log).
        log_level: Livello di log per il messaggio di latenza.
        elapsed_ms: Millisecondi impiegati. Valorizzato all'uscita del contesto.

    Example:
        with LatencyTracker("scene_detection") as tracker:
            result = detector.analyze(frame)
        print(f"Scene detection: {tracker.elapsed_ms:.1f}ms")
    """

    def __init__(
        self,
        name: str,
        log_level: str = "debug",
        extra: dict[str, object] | None = None,
    ) -> None:
        """Inizializza il tracker.

        Args:
            name: Nome dell'operazione da misurare (es. "pipeline.vlm").
            log_level: Livello di log ("debug", "info", "warning").
            extra: Campi aggiuntivi da includere nel log (es. frame_id).
        """
        self.name = name
        self.log_level = log_level
        self.extra = extra or {}
        self.elapsed_ms: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "LatencyTracker":
        """Avvia il timer.

        Returns:
            Self per accesso a ``elapsed_ms`` dopo il blocco.
        """
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Ferma il timer e logga la latenza.

        Args:
            exc_type: Tipo dell'eccezione se presente.
            exc_val: Valore dell'eccezione se presente.
            exc_tb: Traceback dell'eccezione se presente.
        """
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000
        log_fn = getattr(logger, self.log_level, logger.debug)
        log_fn(
            f"latency.{self.name}",
            elapsed_ms=round(self.elapsed_ms, 2),
            **self.extra,
        )

    async def __aenter__(self) -> "LatencyTracker":
        """Avvia il timer (versione asincrona).

        Returns:
            Self per accesso a ``elapsed_ms`` dopo il blocco.
        """
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Ferma il timer e logga la latenza (versione asincrona).

        Args:
            exc_type: Tipo dell'eccezione se presente.
            exc_val: Valore dell'eccezione se presente.
            exc_tb: Traceback dell'eccezione se presente.
        """
        self.__exit__(exc_type, exc_val, exc_tb)


__all__ = ["LatencyTracker"]
