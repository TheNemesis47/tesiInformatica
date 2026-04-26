"""Domain model specifici di object-memory.

FrameData, BoundingBox, Detection e SceneAnalysis sono in vision-commons.
Questo package contiene i modelli del dominio "memoria degli oggetti".
"""

from __future__ import annotations

from object_memory.core.domain.object_record import (
    ObjectLabel,
    ObjectRecord,
    SpatialPosition,
)
from object_memory.core.domain.snapshot import ObjectSnapshot, SnapshotQuery

__all__ = [
    "ObjectLabel",
    "ObjectRecord",
    "ObjectSnapshot",
    "SnapshotQuery",
    "SpatialPosition",
]
