"""Port specifici di object-memory.

SceneDetectorPort, FrameSourcePort e FramePreprocessorPort sono condivisi
e si trovano in vision-commons. Questo package contiene i port
specifici della pipeline di memorizzazione degli oggetti.
"""

from __future__ import annotations

from object_memory.core.ports.object_detector import ObjectDetectorPort
from object_memory.core.ports.object_labeler import ObjectLabelerPort
from object_memory.core.ports.object_repository import ObjectRepositoryPort
from object_memory.core.ports.snapshot_store import SnapshotStorePort

__all__ = [
    "ObjectDetectorPort",
    "ObjectLabelerPort",
    "ObjectRepositoryPort",
    "SnapshotStorePort",
]
