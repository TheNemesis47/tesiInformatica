"""Prompt in italiano per l'etichettatura degli oggetti tramite VLM.

I prompt sono ottimizzati per produrre etichette brevi e uniche che
l'utente possa poi utilizzare nelle query vocali ("dove è la X?").
Enfatizzano: colore, materiale, tipo e caratteristiche distintive.
"""

from __future__ import annotations

PROMPT_LABEL_IT: str = (
    "Sei un assistente per catalogare oggetti in un ambiente domestico. "
    "Guarda l'oggetto evidenziato al centro dell'immagine e descriviLO "
    "con UNA SOLA etichetta breve di 2-4 parole. "
    "Includi: colore + tipo (es. 'maglia rossa', 'bottiglia acqua', 'libro blu'). "
    "Se c'è testo sull'oggetto, includilo (es. 'libro Python', 'bottiglia Coca-Cola'). "
    "NON usare frasi, solo l'etichetta. NON aggiungere punteggiatura finale. "
    "Rispondi SOLO con l'etichetta, nient'altro."
)

PROMPT_LABEL_WITH_CONTEXT_IT: str = (
    "Sei un assistente per catalogare oggetti. "
    "Nell'immagine è evidenziato un oggetto di tipo '{class_name}' "
    "(rilevato dal sistema di object detection). "
    "Dai a questo specifico oggetto un'etichetta di 2-4 parole che lo distingua "
    "dagli altri oggetti simili: includi colore, materiale o caratteristiche uniche. "
    "Es: 'maglia rossa a righe', 'tazza bianca IKEA', 'chiavi con portachiavi verde'. "
    "Rispondi SOLO con l'etichetta."
)

# Alias pubblici
PROMPT_LABEL = PROMPT_LABEL_IT
PROMPT_LABEL_WITH_CONTEXT = PROMPT_LABEL_WITH_CONTEXT_IT

__all__ = [
    "PROMPT_LABEL",
    "PROMPT_LABEL_IT",
    "PROMPT_LABEL_WITH_CONTEXT",
    "PROMPT_LABEL_WITH_CONTEXT_IT",
]
