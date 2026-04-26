"""Client di basso livello per Gemma 4 via Ollama.

Astrae la comunicazione con il server Ollama esponendo un'interfaccia
minimale: immagine + prompt → testo. Non conosce nulla del dominio
specifico (caption vs labeling) — quella logica è nei progetti consumer.

Sia vision-caption (GemmaCaptionGenerator) sia object-memory
(GemmaObjectLabeler) usano questo client, ognuno con i propri prompt.
"""

from __future__ import annotations

import time

import structlog

logger = structlog.get_logger(__name__)


class GemmaVLMClient:
    """Client di basso livello per modelli vision-language via Ollama.

    Invia un'immagine JPEG (bytes) e un prompt testuale al modello Gemma
    in esecuzione su Ollama, restituisce il testo generato.

    Questo è il componente condiviso tra i progetti: ogni progetto consumer
    lo wrappa con la propria logica di dominio (selezione prompt, parsing
    risposta, costruzione domain model).

    Attributes:
        model_name: Identificatore del modello Ollama (es. "gemma4:e4b").
        temperature: Temperatura di campionamento [0.0, 1.0].
        max_tokens: Numero massimo di token da generare.
    """

    def __init__(
        self,
        model_name: str = "gemma4:e4b",
        temperature: float = 0.3,
        max_tokens: int = 150,
    ) -> None:
        """Inizializza il client Gemma.

        Args:
            model_name: Identificatore del modello Ollama.
            temperature: Temperatura per la generazione (0.0–1.0).
            max_tokens: Limite di token per la risposta.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def query(self, image_bytes: bytes, prompt: str) -> tuple[str, float]:
        """Invia immagine + prompt a Gemma e restituisce il testo generato.

        Metodo di basso livello: non interpreta il risultato, non costruisce
        domain model — restituisce solo il testo grezzo e la latenza.

        Args:
            image_bytes: Bytes dell'immagine JPEG da analizzare.
            prompt: Prompt testuale da inviare al modello.

        Returns:
            Tupla (testo_generato, latenza_ms).

        Raises:
            VisionCaptionError: Se Ollama non risponde o restituisce errore.
        """
        # TODO: implementare
        # import base64
        # import ollama
        # 1. Codifica image_bytes in base64
        # 2. t0 = time.perf_counter()
        # 3. response = await ollama.AsyncClient().chat(
        #        model=self.model_name,
        #        messages=[{
        #            "role": "user",
        #            "content": prompt,
        #            "images": [base64.b64encode(image_bytes).decode("utf-8")],
        #        }],
        #        options={"temperature": self.temperature, "num_predict": self.max_tokens},
        #    )
        # 4. latency_ms = (time.perf_counter() - t0) * 1000
        # 5. text = response["message"]["content"].strip()
        # 6. logger.debug("gemma_client.query", latency_ms=round(latency_ms, 1), tokens=len(text.split()))
        # 7. return text, latency_ms
        raise NotImplementedError


__all__ = ["GemmaVLMClient"]
