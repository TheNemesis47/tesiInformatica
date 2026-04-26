"""Test per i template di prompt."""

from __future__ import annotations

from vision_caption.adapters.captioning.prompts.prompt_templates import (
    SUPPORTED_LANGUAGES,
    get_prompt,
)
from vision_commons.domain.frame import CaptureMode


class TestPromptTemplates:
    """Test per la selezione e il contenuto dei prompt."""

    def test_italian_in_supported_languages(self) -> None:
        """L'italiano è supportato."""
        assert "it" in SUPPORTED_LANGUAGES

    def test_get_prompt_auto_it(self) -> None:
        """Il prompt AUTO in italiano è non vuoto e contiene parole chiave."""
        prompt = get_prompt(CaptureMode.AUTO, language="it")
        assert len(prompt) > 50
        assert "ciech" in prompt.lower() or "blind" in prompt.lower() or "ostacoli" in prompt.lower()

    def test_get_prompt_pointing_it(self) -> None:
        """Il prompt POINTING in italiano è non vuoto e diverso da AUTO."""
        auto_prompt = get_prompt(CaptureMode.AUTO, language="it")
        pointing_prompt = get_prompt(CaptureMode.POINTING, language="it")
        assert len(pointing_prompt) > 50
        assert auto_prompt != pointing_prompt

    def test_unsupported_language_fallback_to_italian(self) -> None:
        """Una lingua non supportata fa fallback all'italiano."""
        prompt_it = get_prompt(CaptureMode.AUTO, language="it")
        prompt_unknown = get_prompt(CaptureMode.AUTO, language="xyz")
        assert prompt_it == prompt_unknown

    def test_prompt_contains_no_placeholder(self) -> None:
        """I prompt non contengono placeholder non sostituiti come {variable}."""
        import re
        for mode in CaptureMode:
            prompt = get_prompt(mode, language="it")
            # Cerca pattern {nome_variabile} non sostituiti
            placeholders = re.findall(r"\{[a-z_]+\}", prompt)
            assert placeholders == [], f"Placeholder trovati in {mode}: {placeholders}"
