"""Eccezioni custom per object-memory."""

from __future__ import annotations


class ObjectMemoryError(Exception):
    """Eccezione base per tutti gli errori di object-memory."""


class LabelingError(ObjectMemoryError):
    """Errore nell'etichettatura VLM di un oggetto."""


class RepositoryError(ObjectMemoryError):
    """Errore nell'accesso al database degli oggetti."""


class SnapshotStoreError(ObjectMemoryError):
    """Errore nel salvataggio o recupero degli screenshot."""


__all__ = ["LabelingError", "ObjectMemoryError", "RepositoryError", "SnapshotStoreError"]
