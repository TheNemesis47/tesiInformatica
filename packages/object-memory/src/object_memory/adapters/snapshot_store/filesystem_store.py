"""FileSystem store per gli screenshot degli oggetti."""

from __future__ import annotations

import time
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)


class FileSystemSnapshotStore:
    """Store che salva gli screenshot come file JPEG sul filesystem.

    Organizza i file in directory per oggetto:
        snapshots_dir/<object_id>/<timestamp>.jpg

    Attributes:
        snapshots_dir: Directory radice per gli snapshot.
    """

    def __init__(self, snapshots_dir: Path | str = "data/snapshots") -> None:
        """Inizializza lo store.

        Args:
            snapshots_dir: Directory radice per gli snapshot.
                Viene creata se non esiste.
        """
        self.snapshots_dir = Path(snapshots_dir)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, object_id: str, image_bytes: bytes) -> str:
        """Salva lo screenshot e restituisce il percorso relativo.

        Args:
            object_id: UUID dell'oggetto proprietario.
            image_bytes: Bytes JPEG dello screenshot.

        Returns:
            Percorso relativo del file (stringa).
        """
        # TODO: implementare
        # 1. obj_dir = self.snapshots_dir / object_id
        # 2. obj_dir.mkdir(exist_ok=True)
        # 3. filename = f"{int(time.time() * 1000)}.jpg"
        # 4. file_path = obj_dir / filename
        # 5. file_path.write_bytes(image_bytes)
        # 6. return str(file_path)
        raise NotImplementedError

    async def load(self, snapshot_path: str) -> bytes:
        """Carica lo screenshot dal percorso fornito.

        Args:
            snapshot_path: Percorso restituito da save().

        Returns:
            Bytes JPEG dello screenshot.

        Raises:
            ObjectMemoryError: Se il file non esiste.
        """
        # TODO: implementare
        raise NotImplementedError

    async def delete(self, snapshot_path: str) -> None:
        """Elimina uno screenshot dal filesystem.

        Args:
            snapshot_path: Percorso restituito da save().
        """
        # TODO: implementare
        raise NotImplementedError


__all__ = ["FileSystemSnapshotStore"]
