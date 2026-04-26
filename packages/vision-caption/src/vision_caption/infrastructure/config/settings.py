"""Configurazione centralizzata tramite Pydantic Settings.

Carica la configurazione da un file YAML e supporta override
tramite variabili d'ambiente con prefisso ``VC_``.

Esempio di override via env:
    VC_SERVER__PORT=9000 python -m vision_caption
    VC_VLM__MODEL_NAME=gemma4:27b python -m vision_caption
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """Configurazione del server WebSocket.

    Attributes:
        host: Indirizzo IP su cui ascoltare.
        port: Porta TCP del server WebSocket.
        max_connections: Numero massimo di client connessi simultaneamente.
    """

    model_config = SettingsConfigDict(env_prefix="VC_SERVER__")

    host: str = "0.0.0.0"
    port: int = 8765
    max_connections: int = 1


class CameraSettings(BaseSettings):
    """Configurazione della sorgente video.

    Attributes:
        resolution_width: Larghezza del frame in pixel.
        resolution_height: Altezza del frame in pixel.
        jpeg_quality: Qualità di compressione JPEG [0, 100].
        frame_send_interval_ms: Intervallo in ms tra invii di frame consecutivi
            dal client al server.
    """

    model_config = SettingsConfigDict(env_prefix="VC_CAMERA__")

    resolution_width: int = 1280
    resolution_height: int = 960
    jpeg_quality: int = 75
    frame_send_interval_ms: int = 500


class SceneDetectionSettings(BaseSettings):
    """Configurazione del modulo di scene detection.

    Attributes:
        ssim_threshold: Soglia SSIM sotto la quale la scena è "cambiata".
        semantic_threshold: Soglia di differenza semantica per RF-DETR.
        min_caption_interval_sec: Intervallo minimo tra caption consecutive.
        rfdetr_model_size: Dimensione del modello RF-DETR ("small" o "large").
        rfdetr_confidence: Soglia di confidenza per le detection RF-DETR.
    """

    model_config = SettingsConfigDict(env_prefix="VC_SCENE_DETECTION__")

    ssim_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    semantic_threshold: float = Field(default=0.3, ge=0.0, le=1.0)
    min_caption_interval_sec: float = Field(default=3.0, gt=0.0)
    rfdetr_model_size: str = "small"
    rfdetr_confidence: float = Field(default=0.25, ge=0.0, le=1.0)


class VLMSettings(BaseSettings):
    """Configurazione del modello VLM per la generazione caption.

    Attributes:
        model_name: Identificatore del modello Ollama.
        runtime: Backend di inferenza ("ollama").
        temperature: Temperatura di campionamento [0.0, 1.0].
        max_tokens: Numero massimo di token generati.
        language: Lingua delle caption generate (ISO 639-1).
    """

    model_config = SettingsConfigDict(env_prefix="VC_VLM__")

    model_name: str = "gemma4:e4b"
    runtime: str = "ollama"
    temperature: float = Field(default=0.3, ge=0.0, le=1.0)
    max_tokens: int = Field(default=100, gt=0)
    language: str = "it"


class TTSSettings(BaseSettings):
    """Configurazione del modello TTS per la sintesi vocale.

    Attributes:
        model: Modello TTS da usare.
        language: Lingua della sintesi vocale (ISO 639-1).
        exaggeration: Espressività della voce [0.0, 1.0].
        cfg_weight: Peso del classifier-free guidance [0.0, 1.0].
        output_format: Formato audio di output ("wav" o "opus").
    """

    model_config = SettingsConfigDict(env_prefix="VC_TTS__")

    model: str = "chatterbox-turbo"
    language: str = "it"
    exaggeration: float = Field(default=0.3, ge=0.0, le=1.0)
    cfg_weight: float = Field(default=0.5, ge=0.0, le=1.0)
    output_format: str = "wav"


class GestureSettings(BaseSettings):
    """Configurazione per il riconoscimento dei gesti di puntamento.

    Attributes:
        pointing_debounce_ms: Tempo di debounce in ms per il gesto di puntamento.
        pointing_cooldown_ms: Cooldown in ms tra puntamenti consecutivi.
        pointing_crop_size: Dimensione del crop centrato sul punto indicato.
    """

    model_config = SettingsConfigDict(env_prefix="VC_GESTURES__")

    pointing_debounce_ms: int = 1500
    pointing_cooldown_ms: int = 2000
    pointing_crop_size: int = 320


class LoggingSettings(BaseSettings):
    """Configurazione del logging strutturato.

    Attributes:
        level: Livello di log (DEBUG, INFO, WARNING, ERROR).
        save_frames: Se True, salva i frame su disco per debug.
        save_captions: Se True, salva le caption generate su file.
        log_latency: Se True, logga le metriche di latenza per ogni frame.
    """

    model_config = SettingsConfigDict(env_prefix="VC_LOGGING__")

    level: str = "INFO"
    save_frames: bool = False
    save_captions: bool = True
    log_latency: bool = True


class AppSettings(BaseSettings):
    """Configurazione globale dell'applicazione.

    Aggrega tutti i sotto-moduli di configurazione. Può essere caricata
    da YAML tramite ``load_settings()`` oppure interamente tramite
    variabili d'ambiente con prefisso ``VC_``.
    """

    model_config = SettingsConfigDict(env_prefix="VC_")

    server: ServerSettings = ServerSettings()
    camera: CameraSettings = CameraSettings()
    scene_detection: SceneDetectionSettings = SceneDetectionSettings()
    vlm: VLMSettings = VLMSettings()
    tts: TTSSettings = TTSSettings()
    gestures: GestureSettings = GestureSettings()
    logging: LoggingSettings = LoggingSettings()

    @classmethod
    def from_yaml(cls, config_path: Path | str) -> "AppSettings":
        """Carica la configurazione da un file YAML.

        Il file YAML viene letto e i valori vengono passati al costruttore
        di AppSettings. I campi non presenti nel YAML usano i valori di default.

        Args:
            config_path: Percorso al file YAML di configurazione.

        Returns:
            Istanza di AppSettings con i valori dal YAML.

        Raises:
            ConfigurationError: Se il file non esiste o non è valido YAML.
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            raw: dict[str, object] = yaml.safe_load(f) or {}

        return cls.model_validate(raw)


def load_settings(config_path: str | Path = "config.yaml") -> AppSettings:
    """Carica le impostazioni dell'applicazione.

    Tenta di caricare da YAML; se il file non esiste, usa i valori di default.

    Args:
        config_path: Percorso al file YAML (default: "config.yaml").

    Returns:
        AppSettings con la configurazione caricata.
    """
    path = Path(config_path)
    if path.exists():
        return AppSettings.from_yaml(path)
    return AppSettings()


__all__ = ["AppSettings", "load_settings"]
