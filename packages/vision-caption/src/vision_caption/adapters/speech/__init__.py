"""Speech adapters di vision-caption."""
from __future__ import annotations
from vision_caption.adapters.speech.chatterbox_synth import ChatterboxSynthesizer
from vision_caption.adapters.speech.mock_synth import MockSynthesizer
__all__ = ["ChatterboxSynthesizer", "MockSynthesizer"]
