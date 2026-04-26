"""Adapter per la generazione di caption tramite Gemma 4 via Ollama.

Wrappa il GemmaVLMClient di vision-commons con la logica di dominio
specifica di vision-caption: selezione prompt per modalità/lingua e
costruzione del domain model Caption.
"""

from __future__ import annotations

import structlog

from vision_caption.adapters.captioning.prompts.prompt_templates import get_prompt
from vision_caption.core.domain.caption import Caption, CaptionRequest
from vision_commons.adapters.vlm.gemma_client import GemmaVLMClient

logger = structlog.get_logger(__name__)


class GemmaCaptionGenerator:
    """Generatore di caption tramite Gemma 4 (VLM) via Ollama.

    Wrappa GemmaVLMClient (vision-commons) con logica specifica di
    vision-caption: selezione del prompt per modalità/lingua, parsing
    del testo grezzo in Caption domain model.

    Attributes:
        language: Lingua delle caption generate (codice ISO 639-1).
        _vlm: Client VLM di basso livello da vision-commons.
    """

    def __init__(
        self,
        model_name: str = "gemma4:e4b",
        temperature: float = 0.3,
        max_tokens: int = 100,
        language: str = "it",
        vlm_client: GemmaVLMClient | None = None,
    ) -> None:
        """Inizializza il generatore Gemma.

        Args:
            model_name: Identificatore del modello Ollama.
            temperature: Temperatura per la generazione (0.0–1.0).
            max_tokens: Limite di token per la risposta.
            language: Lingua target per la caption (es. "it", "en").
            vlm_client: Client VLM da iniettare. Se None, ne crea uno
                con i parametri forniti (utile per testabilità).
        """
        self.language = language
        self._vlm = vlm_client or GemmaVLMClient(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def generate(self, request: CaptionRequest) -> Caption:
        """Genera una caption per il frame tramite Gemma 4 via Ollama.

        Args:
            request: Richiesta contenente il frame e la modalità.

        Returns:
            Caption con il testo generato e la latenza.

        Raises:
            CaptionGenerationError: Se il VLM non risponde o restituisce errore.
        """
        # TODO: implementare
        # 1. prompt = request.prompt_override or get_prompt(request.mode, self.language)
        # 2. text, latency_ms = await self._vlm.query(request.frame.image_bytes, prompt)
        # 3. logger.debug("caption.generated", mode=request.mode, latency_ms=latency_ms)
        # 4. return Caption(text=text, mode=request.mode, language=self.language,
        #                   generation_time_ms=latency_ms)
        raise NotImplementedError


__all__ = ["GemmaCaptionGenerator"]
