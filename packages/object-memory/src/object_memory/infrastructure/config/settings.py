"""Configurazione centralizzata di object-memory tramite Pydantic Settings."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """Configurazione del server WebSocket e REST."""

    model_config = SettingsConfigDict(env_prefix="OM_SERVER__")

    host: str = "0.0.0.0"
    port: int = 8766
    max_connections: int = 1


class CameraSettings(BaseSettings):
    """Configurazione della sorgente video."""

    model_config = SettingsConfigDict(env_prefix="OM_CAMERA__")

    resolution_width: int = 1280
    resolution_height: int = 960
    jpeg_quality: int = 75
    frame_send_interval_ms: int = 500


class SceneDetectionSettings(BaseSettings):
    """Configurazione del filtro SSIM."""

    model_config = SettingsConfigDict(env_prefix="OM_SCENE_DETECTION__")

    ssim_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    min_catalog_interval_sec: float = Field(default=2.0, gt=0.0)
    rfdetr_model_size: str = "small"
    rfdetr_confidence: float = Field(default=0.35, ge=0.0, le=1.0)


class VLMSettings(BaseSettings):
    """Configurazione del VLM per l'etichettatura."""

    model_config = SettingsConfigDict(env_prefix="OM_VLM__")

    model_name: str = "gemma4:e4b"
    runtime: str = "ollama"
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens: int = Field(default=50, gt=0)
    language: str = "it"


class StorageSettings(BaseSettings):
    """Configurazione della persistenza (DB + snapshot)."""

    model_config = SettingsConfigDict(env_prefix="OM_STORAGE__")

    db_path: str = "data/object_memory.db"
    snapshots_dir: str = "data/snapshots"
    max_snapshots_per_object: int = 10


class OverlapSettings(BaseSettings):
    """Configurazione del tracker di overlap."""

    model_config = SettingsConfigDict(env_prefix="OM_OVERLAP__")

    iou_threshold: float = Field(default=0.4, ge=0.0, le=1.0)
    position_update_threshold: float = Field(default=0.15, ge=0.0, le=1.0)


class LoggingSettings(BaseSettings):
    """Configurazione del logging."""

    model_config = SettingsConfigDict(env_prefix="OM_LOGGING__")

    level: str = "INFO"
    save_frames: bool = False
    log_latency: bool = True


class AppSettings(BaseSettings):
    """Configurazione globale di object-memory."""

    model_config = SettingsConfigDict(env_prefix="OM_")

    server: ServerSettings = ServerSettings()
    camera: CameraSettings = CameraSettings()
    scene_detection: SceneDetectionSettings = SceneDetectionSettings()
    vlm: VLMSettings = VLMSettings()
    storage: StorageSettings = StorageSettings()
    overlap: OverlapSettings = OverlapSettings()
    logging: LoggingSettings = LoggingSettings()

    @classmethod
    def from_yaml(cls, config_path: Path | str) -> "AppSettings":
        """Carica la configurazione da un file YAML.

        Args:
            config_path: Percorso al file YAML.

        Returns:
            AppSettings con i valori dal YAML.

        Raises:
            FileNotFoundError: Se il file non esiste.
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            raw: dict[str, object] = yaml.safe_load(f) or {}
        return cls.model_validate(raw)


def load_settings(config_path: str | Path = "config.yaml") -> AppSettings:
    """Carica le impostazioni, con fallback ai default."""
    path = Path(config_path)
    if path.exists():
        return AppSettings.from_yaml(path)
    return AppSettings()


__all__ = ["AppSettings", "load_settings"]
