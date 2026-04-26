"""Template di prompt per l'etichettatura degli oggetti."""

from __future__ import annotations

from object_memory.adapters.labeling.prompts import it as prompts_it
from vision_commons.domain.detection import Detection

_REGISTRY: dict[str, object] = {"it": prompts_it}
SUPPORTED_LANGUAGES: frozenset[str] = frozenset(_REGISTRY.keys())


def get_label_prompt(detection: Detection, language: str = "it") -> str:
    """Restituisce il prompt per l'etichettatura di un oggetto.

    Args:
        detection: Detection dell'oggetto da etichettare. Il class_name
            può essere inserito nel prompt contestuale.
        language: Codice lingua ISO 639-1.

    Returns:
        Prompt da inviare al VLM.
    """
    lang_module = _REGISTRY.get(language, prompts_it)
    template = str(getattr(lang_module, "PROMPT_LABEL_WITH_CONTEXT", prompts_it.PROMPT_LABEL_WITH_CONTEXT_IT))
    return template.format(class_name=detection.class_name)


__all__ = ["SUPPORTED_LANGUAGES", "get_label_prompt"]
