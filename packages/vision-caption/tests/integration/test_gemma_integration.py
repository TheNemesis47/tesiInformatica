"""Test di integrazione con Gemma 4 via Ollama.

Questi test richiedono un server Ollama in esecuzione con il modello
gemma4:e4b scaricato. Vengono saltati automaticamente se Ollama non
è raggiungibile.

Per eseguirli manualmente:
    ollama pull gemma4:e4b
    ollama serve
    pytest tests/integration/test_gemma_integration.py -v
"""

from __future__ import annotations

import pytest

from vision_caption.adapters.captioning.gemma_caption import GemmaCaptionGenerator
from vision_caption.core.domain.caption import CaptionRequest
from vision_commons.domain.frame import CaptureMode, FrameData


def _ollama_available() -> bool:
    """Verifica se Ollama è raggiungibile su localhost."""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _ollama_available(),
    reason="Ollama non raggiungibile su localhost:11434",
)


class TestGemmaIntegration:
    """Test di integrazione con il modello Gemma via Ollama."""

    @pytest.mark.asyncio
    async def test_generate_caption_auto_mode(
        self,
        mock_frame_data: FrameData,
    ) -> None:
        """Genera una caption in modalità AUTO con frame reale."""
        generator = GemmaCaptionGenerator(model_name="gemma4:e4b")
        request = CaptionRequest(frame=mock_frame_data, mode=CaptureMode.AUTO)

        # TODO: decommentare quando GemmaCaptionGenerator.generate() è implementato
        # caption = await generator.generate(request)
        # assert len(caption.text) > 10
        # assert caption.language == "it"
        # assert caption.generation_time_ms > 0
        pytest.skip("GemmaCaptionGenerator.generate() non ancora implementato")
