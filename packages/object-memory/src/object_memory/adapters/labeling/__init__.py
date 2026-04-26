"""Labeling adapters di object-memory."""
from __future__ import annotations
from object_memory.adapters.labeling.gemma_labeler import GemmaObjectLabeler
from object_memory.adapters.labeling.mock_labeler import MockObjectLabeler
__all__ = ["GemmaObjectLabeler", "MockObjectLabeler"]
