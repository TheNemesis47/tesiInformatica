"""Domain model specifici di vision-caption.

FrameData, BoundingBox, Detection e SceneAnalysis sono condivisi
e si trovano in ``vision_commons.domain``. Questo package contiene
solo i modelli specifici della pipeline di audio-descrizione.
"""

from __future__ import annotations

from vision_caption.core.domain.audio import AudioFormat, AudioResult
from vision_caption.core.domain.caption import Caption, CaptionRequest

__all__ = ["AudioFormat", "AudioResult", "Caption", "CaptionRequest"]
