"""Eccezioni custom per il progetto vision-caption.

Gerarchia delle eccezioni:
    VisionCaptionError (base)
    ├── SceneDetectionError
    ├── CaptionGenerationError
    ├── SpeechSynthesisError
    ├── FrameCaptureError
    └── ConfigurationError
"""

from __future__ import annotations


class VisionCaptionError(Exception):
    """Eccezione base per tutti gli errori del progetto vision-caption.

    Tutte le eccezioni specifiche del progetto ereditano da questa classe,
    permettendo di gestire qualsiasi errore dell'applicazione con un singolo
    ``except VisionCaptionError``.
    """


class SceneDetectionError(VisionCaptionError):
    """Errore nel componente di scene detection.

    Sollevato quando il rilevamento del cambiamento di scena fallisce,
    es. per un frame corrotto o un modello non caricato.
    """


class CaptionGenerationError(VisionCaptionError):
    """Errore nella generazione della caption tramite VLM.

    Sollevato quando il modello VLM (Gemma via Ollama) non risponde,
    restituisce un errore o produce output non valido.
    """


class SpeechSynthesisError(VisionCaptionError):
    """Errore nella sintesi vocale tramite TTS.

    Sollevato quando il modello TTS (Chatterbox) non è disponibile
    o la sintesi dell'audio fallisce.
    """


class FrameCaptureError(VisionCaptionError):
    """Errore nell'acquisizione di un frame dalla sorgente.

    Sollevato quando la webcam non è accessibile, il file video
    non esiste o l'acquisizione restituisce un frame vuoto.
    """


class ConfigurationError(VisionCaptionError):
    """Errore nella configurazione dell'applicazione.

    Sollevato quando il file config.yaml non esiste, non è valido YAML
    o contiene valori fuori range (es. ssim_threshold > 1.0).
    """


__all__ = [
    "CaptionGenerationError",
    "ConfigurationError",
    "FrameCaptureError",
    "SceneDetectionError",
    "SpeechSynthesisError",
    "VisionCaptionError",
]
