"""Port specifici di vision-caption.

SceneDetectorPort, FrameSourcePort e FramePreprocessorPort sono condivisi
e si trovano in ``vision_commons.ports``. Questo package contiene solo
i port specifici della pipeline di audio-descrizione.
"""

from __future__ import annotations

from vision_caption.core.ports.audio_encoder import AudioEncoderPort
from vision_caption.core.ports.caption_generator import CaptionGeneratorPort
from vision_caption.core.ports.speech_synthesizer import SpeechSynthesizerPort

__all__ = ["AudioEncoderPort", "CaptionGeneratorPort", "SpeechSynthesizerPort"]
