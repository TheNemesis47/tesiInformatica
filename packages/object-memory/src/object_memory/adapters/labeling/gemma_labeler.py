"""Adapter per l'etichettatura degli oggetti tramite Gemma 4 via Ollama.

Wrappa GemmaVLMClient (vision-commons) con logica specifica di object-memory:
ritaglia il crop dell'oggetto, seleziona il prompt di labeling, e converte
il testo grezzo in ObjectLabel domain model.
"""

from __future__ import annotations

import structlog

from object_memory.adapters.labeling.prompts.prompt_templates import get_label_prompt
from object_memory.core.domain.object_record import ObjectLabel
from vision_commons.adapters.vlm.gemma_client import GemmaVLMClient
from vision_commons.domain.detection import Detection
from vision_commons.domain.frame import FrameData

logger = structlog.get_logger(__name__)


class GemmaObjectLabeler:
    """Etichettatore di oggetti tramite Gemma 4 (VLM) via Ollama.

    Usa GemmaVLMClient (vision-commons) per l'accesso al modello.
    Ritaglia il crop dell'oggetto dalla bounding box prima di inviarlo
    al VLM per ridurre il contesto visivo e migliorare la precisione
    dell'etichetta.

    Attributes:
        language: Lingua delle etichette generate.
        _vlm: Client VLM di basso livello da vision-commons.
    """

    def __init__(
        self,
        model_name: str = "gemma4:e4b",
        temperature: float = 0.1,
        max_tokens: int = 20,
        language: str = "it",
        vlm_client: GemmaVLMClient | None = None,
    ) -> None:
        """Inizializza il labeler Gemma.

        Args:
            model_name: Identificatore del modello Ollama.
            temperature: Temperatura bassa per etichette più deterministiche.
            max_tokens: Pochi token sufficienti per etichette brevi.
            language: Lingua target per le etichette.
            vlm_client: Client VLM da iniettare (utile per testabilità).
        """
        self.language = language
        self._vlm = vlm_client or GemmaVLMClient(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def label(
        self,
        frame: FrameData,
        detection: Detection,
        language: str = "it",
    ) -> ObjectLabel:
        """Assegna un'etichetta semantica all'oggetto rilevato.

        Args:
            frame: Frame originale (per il crop della detection).
            detection: Detection dell'oggetto da etichettare.
            language: Lingua dell'etichetta da generare.

        Returns:
            ObjectLabel con il testo descrittivo dell'oggetto.

        Raises:
            ObjectMemoryError: Se il VLM non risponde o l'etichettatura fallisce.
        """
        # TODO: implementare
        # 1. Ritaglia il crop dell'oggetto dal frame usando detection.bbox
        #    (usa cv2.imdecode + slicing + cv2.imencode)
        # 2. prompt = get_label_prompt(detection, language or self.language)
        # 3. text, latency_ms = await self._vlm.query(crop_bytes, prompt)
        # 4. label_text = text.strip().lower()  # normalizza
        # 5. logger.debug("object.labeled", label=label_text, latency_ms=latency_ms)
        # 6. return ObjectLabel(text=label_text, language=language or self.language)
        raise NotImplementedError


__all__ = ["GemmaObjectLabeler"]
