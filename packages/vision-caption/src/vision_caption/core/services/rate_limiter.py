"""Rate limiter per il throttling delle caption generate.

Limita la frequenza con cui la pipeline genera nuove caption per evitare
di sovraccaricare l'utente con descrizioni troppo ravvicinate.
"""

from __future__ import annotations

import time


class RateLimiter:
    """Throttler semplice basato su intervallo minimo tra eventi.

    Mantiene il timestamp dell'ultimo evento registrato e permette un
    nuovo evento solo se è trascorso almeno ``min_interval_sec`` secondi.

    Attributes:
        min_interval_sec: Intervallo minimo in secondi tra due caption
            consecutive. Configurabile tramite AppSettings.
    """

    def __init__(self, min_interval_sec: float) -> None:
        """Inizializza il rate limiter.

        Args:
            min_interval_sec: Intervallo minimo in secondi tra due eventi
                consecutivi. Valori tipici: 2.0–5.0 secondi.
        """
        self.min_interval_sec = min_interval_sec
        self._last_proceed_time: float = 0.0

    def can_proceed(self) -> bool:
        """Verifica se è possibile procedere con un nuovo evento.

        Returns:
            True se è trascorso almeno ``min_interval_sec`` secondi
            dall'ultimo ``record()``, False altrimenti.
        """
        return (time.time() - self._last_proceed_time) >= self.min_interval_sec

    def record(self) -> None:
        """Registra il timestamp dell'evento corrente.

        Deve essere chiamato immediatamente dopo aver verificato
        ``can_proceed() == True`` per aggiornare il riferimento temporale.
        """
        self._last_proceed_time = time.time()

    @property
    def seconds_until_next(self) -> float:
        """Secondi rimanenti prima che il prossimo evento sia consentito.

        Returns:
            0.0 se si può procedere subito, altrimenti i secondi da attendere.
        """
        elapsed = time.time() - self._last_proceed_time
        remaining = self.min_interval_sec - elapsed
        return max(0.0, remaining)


__all__ = ["RateLimiter"]
