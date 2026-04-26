"""Port per lo storage degli screenshot degli oggetti.

Gestisce il salvataggio e il recupero dei file immagine (JPEG) associati
agli oggetti memorizzati. Implementato da FileSystemSnapshotStore.
"""

from __future__ import annotations

from typing import Protocol


class SnapshotStorePort(Protocol):
    """Interfaccia per lo storage degli screenshot degli oggetti.

    Separa la logica di accesso ai file dal dominio, permettendo di usare
    filesystem locale in sviluppo e object storage (S3, MinIO) in produzione.
    """

    async def save(self, object_id: str, image_bytes: bytes) -> str:
        """Salva lo screenshot di un oggetto e restituisce il percorso.

        Il percorso restituito viene poi salvato in ObjectRecord.last_snapshot_path
        e usato per recuperare l'immagine nelle query.

        Args:
            object_id: UUID dell'oggetto proprietario dello screenshot.
            image_bytes: Bytes JPEG dello screenshot ritagliato dell'oggetto.

        Returns:
            Percorso (stringa) con cui recuperare lo snapshot in futuro.
        """
        ...

    async def load(self, snapshot_path: str) -> bytes:
        """Carica lo screenshot dal percorso fornito.

        Args:
            snapshot_path: Percorso restituito da ``save()``.

        Returns:
            Bytes JPEG dello screenshot.

        Raises:
            ObjectMemoryError: Se il file non esiste o non è leggibile.
        """
        ...

    async def delete(self, snapshot_path: str) -> None:
        """Elimina uno screenshot dal filesystem.

        Args:
            snapshot_path: Percorso restituito da ``save()``.
        """
        ...


__all__ = ["SnapshotStorePort"]
