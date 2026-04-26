"""Captioning adapters di vision-caption."""
from __future__ import annotations
from vision_caption.adapters.captioning.gemma_caption import GemmaCaptionGenerator
from vision_caption.adapters.captioning.mock_caption import MockCaptionGenerator
__all__ = ["GemmaCaptionGenerator", "MockCaptionGenerator"]
