"""Adapter per il rilevamento ibrido di cambiamenti di scena.

Combina SSIM (veloce, pixel-level) e RF-DETR (preciso, semantico)
in una pipeline a due stadi: SSIM filtra i frame non cambiati rapidamente,
RF-DETR analizza solo quelli che passano il filtro SSIM.

Questa strategia bilancia latenza e precisione: RF-DETR (costoso) viene
invocato solo quando SSIM indica un possibile cambiamento.
"""

from __future__ import annotations

import structlog

from vision_commons.adapters.scene_detection.rfdetr_detector import RFDETRSceneDetector
from vision_commons.adapters.scene_detection.ssim_detector import SSIMSceneDetector
from vision_commons.domain.detection import SceneAnalysis
from vision_commons.domain.frame import FrameData

logger = structlog.get_logger(__name__)


class HybridSceneDetector:
    """Rilevatore ibrido SSIM + RF-DETR per massima accuratezza.

    Strategia a due stadi:
    1. SSIM: filtro veloce — se SSIM è alto (scena invariata), skip RF-DETR
    2. RF-DETR: analisi semantica — solo per i frame che passano il filtro SSIM

    Usa composizione (non ereditarietà) per combinare i due detector.

    Attributes:
        ssim_detector: Detector SSIM per il filtro rapido.
        rfdetr_detector: Detector RF-DETR per l'analisi semantica.
    """

    def __init__(
        self,
        ssim_detector: SSIMSceneDetector,
        rfdetr_detector: RFDETRSceneDetector,
    ) -> None:
        """Inizializza il detector ibrido con i due detector iniettati.

        Args:
            ssim_detector: Istanza configurata di SSIMSceneDetector.
            rfdetr_detector: Istanza configurata di RFDETRSceneDetector.
        """
        self.ssim_detector = ssim_detector
        self.rfdetr_detector = rfdetr_detector

    def analyze(self, frame: FrameData) -> SceneAnalysis:
        """Analizza un frame con la strategia ibrida SSIM → RF-DETR.

        Args:
            frame: Frame corrente da analizzare.

        Returns:
            SceneAnalysis che integra i risultati di entrambi i detector.
            Se SSIM indica nessun cambiamento, RF-DETR non viene eseguito
            e ``semantic_diff`` è None. Se SSIM indica cambiamento, RF-DETR
            viene eseguito e ``scene_changed`` riflette la sua valutazione.
        """

        ssim_analysis = self.ssim_detector.analyze(frame)
        if not ssim_analysis.scene_changed:
            logger.debug(
                "hybrid_detector.ssim_stable_skipping_rfdetr",
                ssim_score=ssim_analysis.ssim_score
            )
            return ssim_analysis

        logger.info(
            "ssim_analysis, scene changed, skip to RF-DETR",
            ssim_score=ssim_analysis.ssim_score
        )

        rfdetr_analysis = self.rfdetr_detector.analyze(frame)
        combined_analysis = SceneAnalysis(
            detections=rfdetr_analysis.detections,
            scene_changed=rfdetr_analysis.scene_changed,
            ssim_score=ssim_analysis.ssim_score,
            semantic_diff=rfdetr_analysis.semantic_diff
        )
        logger.info(
            "hybrid_detector.analysis_complete",
            scene_changed=combined_analysis.scene_changed,
            ssim_score=combined_analysis.ssim_score,
            semantic_diff=combined_analysis.semantic_diff,
            num_detections=len(combined_analysis.detections)
        )

        return combined_analysis

__all__ = ["HybridSceneDetector"]
