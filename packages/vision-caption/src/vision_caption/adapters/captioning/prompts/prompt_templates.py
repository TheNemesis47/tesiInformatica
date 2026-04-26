"""Template di prompt per la generazione caption multilingua.

Gestisce la selezione del prompt corretto in base alla lingua e alla
modalità di cattura. Aggiungere una nuova lingua richiede solo di
creare un modulo ``<lingua>.py`` e registrarlo nel dizionario ``_REGISTRY``.
"""

from __future__ import annotations

from vision_caption.adapters.captioning.prompts import it as prompts_it
from vision_commons.domain.frame import CaptureMode

# Registro dei moduli di prompt per lingua
# Aggiungere nuove lingue registrandole qui con il codice ISO 639-1
_REGISTRY: dict[str, object] = {
    "it": prompts_it,
}

# Lingue supportate (usato per validazione in AppSettings)
SUPPORTED_LANGUAGES: frozenset[str] = frozenset(_REGISTRY.keys())


def get_prompt(mode: CaptureMode, language: str = "it") -> str:
    """Restituisce il prompt appropriato per la modalità e la lingua.

    Args:
        mode: Modalità di cattura (AUTO o POINTING).
        language: Codice lingua ISO 639-1. Se la lingua non è supportata,
            fallback all'italiano.

    Returns:
        Stringa del prompt da inviare al VLM.
    """
    lang_module = _REGISTRY.get(language, prompts_it)

    match mode:
        case CaptureMode.AUTO:
            return str(getattr(lang_module, "PROMPT_AUTO", prompts_it.PROMPT_AUTO_IT))
        case CaptureMode.POINTING:
            return str(
                getattr(lang_module, "PROMPT_POINTING", prompts_it.PROMPT_POINTING_IT)
            )
        case _:
            return str(getattr(lang_module, "PROMPT_AUTO", prompts_it.PROMPT_AUTO_IT))


__all__ = ["SUPPORTED_LANGUAGES", "get_prompt"]
