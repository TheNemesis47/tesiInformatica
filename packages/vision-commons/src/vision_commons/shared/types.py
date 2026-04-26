"""Type aliases globali per il progetto vision-caption.

Centralizza gli alias di tipo per migliorare la leggibilità del codice
e facilitare futuri refactoring (es. cambiare la rappresentazione di ImageBytes).
"""

from __future__ import annotations

from typing import NewType

# Bytes di un'immagine compressa (JPEG o PNG)
ImageBytes = NewType("ImageBytes", bytes)

# Codice lingua ISO 639-1 (es. "it", "en", "fr")
LanguageCode = NewType("LanguageCode", str)

# Durata o latenza in millisecondi
Milliseconds = NewType("Milliseconds", float)

__all__ = ["ImageBytes", "LanguageCode", "Milliseconds"]
