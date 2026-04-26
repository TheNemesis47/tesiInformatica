"""Port per il rilevamento di cambiamenti nella scena.

Definisce il contratto che ogni implementazione di scene detector deve
rispettare. Le implementazioni concrete (SSIM, RF-DETR, Hybrid) si trovano
in ``adapters.scene_detection``.
"""

from __future__ import annotations

from typing import Protocol

from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData


class SceneDetectorPort(Protocol):
    """Interfaccia per il rilevamento di cambiamenti nella scena.

    Implementazioni concrete determinano SE un frame ricevuto
    rappresenta un cambiamento significativo rispetto allo stato
    precedente della scena.

    Il detector è stateful: mantiene internamente un riferimento
    all'ultimo frame analizzato per calcolare la differenza.
    """

    def analyze(self, frame: FrameData) -> SceneAnalysis:
        """Analizza un frame e determina se la scena è cambiata.

        Args:
            frame: Il frame da analizzare.

        Returns:
            SceneAnalysis con il risultato dell'analisi, includendo
            ``scene_changed=True`` se la scena è cambiata abbastanza
            da giustificare una nuova caption.
        """
        ...


__all__ = ["SceneDetectorPort"]
