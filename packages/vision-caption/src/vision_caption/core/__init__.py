"""Package core di vision-caption — dominio specifico per audio-descrizione.

Il core non importa mai librerie esterne né vision-commons.adapters.
Usa vision-commons solo per i domain model condivisi (FrameData, Detection)
e per i port condivisi (SceneDetectorPort, FrameSourcePort).
"""

from __future__ import annotations

__all__: list[str] = []
