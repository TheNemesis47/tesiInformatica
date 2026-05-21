"""Adapter per il rilevamento di cambiamenti di scena tramite RF-DETR.

Usa RF-DETR (Real-time Detection Transformer) per rilevare gli oggetti
nella scena e confronta le detection tra frame consecutivi per determinare
se la scena è semanticamente cambiata.
"""

from __future__ import annotations

import structlog
import cv2
import numpy as np
import rfdetr

from vision_commons.domain.detection import Detection, SceneAnalysis, BoundingBox
from vision_commons.domain.frame import FrameData
from typing import TYPE_CHECKING

logger = structlog.get_logger(__name__)

if TYPE_CHECKING:
    import rfdetr

class RFDETRSceneDetector:
    """Rilevatore di cambiamenti di scena basato su RF-DETR.

    Usa RF-DETR per l'object detection e confronta la distribuzione
    degli oggetti rilevati tra frame consecutivi per stimare la
    differenza semantica della scena.

    Attributes:
        model_size: Dimensione del modello RF-DETR ("small" o "large").
            "small" è ottimale per latenza, "large" per accuratezza.
        confidence_threshold: Soglia di confidenza minima per accettare
            una detection come valida.
    """

    def __init__(
        self,
        model_size: str = "large",
        confidence_threshold: float = 0.25,
        semantic_threshold: float = 0.35,
    ) -> None:
        """Inizializza il detector RF-DETR.

        Args:
            model_size: Dimensione del modello RF-DETR ("small" o "large").
            confidence_threshold: Confidenza minima per le detection
                nell'intervallo [0, 1].
        """
        self.model_size = model_size
        self.confidence_threshold = confidence_threshold
        self.semantic_threshold = semantic_threshold
        self._model: rfdetr.RFDETRBase | None = None  # rfdetr.RFDETRSmall o RFDETRLarge
        self._last_detections: tuple[Detection, ...] = ()

    def _load_model(self) -> None:
        """Carica il modello RF-DETR in memoria (lazy loading).

        Il caricamento avviene al primo utilizzo per evitare di rallentare
        lo startup dell'applicazione.
        """

        if self._model is "small":
            self._model = rfdetr.RFDETRSmall()
        else:
            self._model = rfdetr.RFDETRLarge()

        #ottimizzazione per la latenza
        if hasattr(self._model, "optimize_for_inference"):
            self._model.optimize_for_inference()
        logger.info("RF-DETR model loaded.")

    def analyze(self, frame: FrameData) -> SceneAnalysis:
        """Analizza un frame con RF-DETR e calcola la differenza semantica.

        Args:
            frame: Frame corrente da analizzare.

        Returns:
            SceneAnalysis con le ``detections`` rilevate, ``semantic_diff``
            valorizzato e ``scene_changed`` in base alla differenza semantica.
        """

        if self._model is None:
            self._load_model()

        #decodifica Byte
        np_arr = np.frombuffer(frame.image_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        #convert BGR -> RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        predictions = self._model.predict(img_rgb, threshold=self.confidence_threshold)
        detections_list = []
        if hasattr(predictions, "xyxy") and len(predictions) > 0:
            for i in range(len(predictions)):
                xyxy = predictions.xyxy[i]
                confidence = float(predictions.confidence[i])
                class_name = str(predictions.data["class_name"][i])
                bbox = BoundingBox(
                    x1 = float(xyxy[0]),
                    y1 = float(xyxy[1]),
                    x2 = float(xyxy[2]),
                    y2 = float(xyxy[3]),
                )
                detections_list.append(Detection(
                    class_name=class_name,
                    confidence=confidence,
                    bbox=bbox
                ))
            detections = tuple(detections_list)

            #calcolo differenza semantica (Jaccard Distance)
            current_classes = set(d.class_name for d in detections)
            last_classes = set(d.class_name for d in self._last_detections)
            if not current_classes and not last_classes:
                semantic_diff = 0.0
            else:
                unione = current_classes.union(last_classes)
                intersezione = current_classes.intersection(last_classes)
                semantic_diff = 1.0 - (len(intersezione) / len(unione))

            #determina se la scena é cambiata
            #primo frame = cambiata
            is_first_frame = len(self._last_detections) == 0 and len(detections) > 0
            scene_changed = is_first_frame or (semantic_diff > self.semantic_threshold)

            self._last_detections = detections

            logger.info(
                "rfdetr.analysis done",
                detected_objects=list(current_classes),
                semantic_diff=semantic_diff,
                threshold=self.confidence_threshold,
                scene_changed=scene_changed
            )

            return SceneAnalysis(detections=detections, scene_changed=scene_changed, semantic_diff=semantic_diff)

__all__ = ["RFDETRSceneDetector"]
