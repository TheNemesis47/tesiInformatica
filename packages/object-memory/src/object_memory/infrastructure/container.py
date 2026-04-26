"""DI Container di object-memory — assembla ports e adapters.

Unico punto dell'applicazione dove gli adapter concreti vengono istanziati
e iniettati nella pipeline e nel query service.
"""

from __future__ import annotations

import structlog

from object_memory.adapters.labeling.gemma_labeler import GemmaObjectLabeler
from object_memory.adapters.labeling.mock_labeler import MockObjectLabeler
from object_memory.adapters.repository.mock_repository import MockObjectRepository
from object_memory.adapters.repository.sqlite_repository import SQLiteObjectRepository
from object_memory.adapters.snapshot_store.filesystem_store import FileSystemSnapshotStore
from object_memory.adapters.snapshot_store.mock_store import MockSnapshotStore
from object_memory.core.ports.object_detector import ObjectDetectorPort
from object_memory.core.ports.object_labeler import ObjectLabelerPort
from object_memory.core.ports.object_repository import ObjectRepositoryPort
from object_memory.core.ports.snapshot_store import SnapshotStorePort
from object_memory.core.services.memory_pipeline import ObjectMemoryPipeline
from object_memory.core.services.overlap_tracker import OverlapTracker
from object_memory.core.services.query_service import ObjectQueryService
from object_memory.infrastructure.config.settings import AppSettings
from vision_commons.adapters.frame_source.webcam_source import WebcamFrameSource
from vision_commons.adapters.scene_detection.hybrid_detector import HybridSceneDetector
from vision_commons.adapters.scene_detection.rfdetr_detector import RFDETRSceneDetector
from vision_commons.adapters.scene_detection.ssim_detector import SSIMSceneDetector
from vision_commons.ports.frame_source import FrameSourcePort
from vision_commons.ports.scene_detector import SceneDetectorPort

logger = structlog.get_logger(__name__)


class ObjectMemoryContainer:
    """DI container per object-memory.

    Attributes:
        settings: Configurazione dell'applicazione.
        use_mocks: Se True, usa adapter mock (senza GPU/DB) per test.
    """

    def __init__(self, settings: AppSettings, use_mocks: bool = False) -> None:
        """Inizializza il container.

        Args:
            settings: Configurazione caricata da YAML/env.
            use_mocks: Se True, sostituisce Gemma, SQLite e filesystem con mock.
        """
        self.settings = settings
        self.use_mocks = use_mocks

        self._scene_detector: SceneDetectorPort | None = None
        self._object_labeler: ObjectLabelerPort | None = None
        self._repository: ObjectRepositoryPort | None = None
        self._snapshot_store: SnapshotStorePort | None = None
        self._overlap_tracker: OverlapTracker | None = None
        self._frame_source: FrameSourcePort | None = None
        self._pipeline: ObjectMemoryPipeline | None = None
        self._query_service: ObjectQueryService | None = None

        logger.info("container.initialized", use_mocks=use_mocks)

    def create_scene_detector(self) -> SceneDetectorPort:
        """Crea il detector di scena (HybridSceneDetector da vision-commons)."""
        if self._scene_detector is None:
            sd = self.settings.scene_detection
            ssim = SSIMSceneDetector(threshold=sd.ssim_threshold)
            rfdetr = RFDETRSceneDetector(
                model_size=sd.rfdetr_model_size,
                confidence_threshold=sd.rfdetr_confidence,
            )
            self._scene_detector = HybridSceneDetector(ssim, rfdetr)
            logger.info("container.scene_detector_created")
        return self._scene_detector

    def create_object_detector(self) -> ObjectDetectorPort:
        """Crea il detector RF-DETR per le bounding box.

        Nota: RF-DETR è lo stesso usato in vision-commons come HybridSceneDetector,
        ma qui lo usiamo direttamente come ObjectDetectorPort per estrarre le detection.
        """
        # TODO: wrappare RFDETRSceneDetector come ObjectDetectorPort
        # (adattare analyze() → detect() che restituisce solo tuple[Detection, ...])
        raise NotImplementedError

    def create_object_labeler(self) -> ObjectLabelerPort:
        """Crea il labeler VLM."""
        if self._object_labeler is None:
            if self.use_mocks:
                self._object_labeler = MockObjectLabeler()
                logger.info("container.labeler_created", type="mock")
            else:
                vlm = self.settings.vlm
                self._object_labeler = GemmaObjectLabeler(
                    model_name=vlm.model_name,
                    temperature=vlm.temperature,
                    max_tokens=vlm.max_tokens,
                    language=vlm.language,
                )
                logger.info("container.labeler_created", type="gemma", model=vlm.model_name)
        return self._object_labeler

    def create_repository(self) -> ObjectRepositoryPort:
        """Crea il repository DB."""
        if self._repository is None:
            if self.use_mocks:
                self._repository = MockObjectRepository()
                logger.info("container.repository_created", type="mock")
            else:
                self._repository = SQLiteObjectRepository(
                    db_path=self.settings.storage.db_path
                )
                logger.info("container.repository_created", type="sqlite")
        return self._repository

    def create_snapshot_store(self) -> SnapshotStorePort:
        """Crea lo snapshot store."""
        if self._snapshot_store is None:
            if self.use_mocks:
                self._snapshot_store = MockSnapshotStore()
                logger.info("container.snapshot_store_created", type="mock")
            else:
                self._snapshot_store = FileSystemSnapshotStore(
                    snapshots_dir=self.settings.storage.snapshots_dir
                )
                logger.info("container.snapshot_store_created", type="filesystem")
        return self._snapshot_store

    def create_overlap_tracker(self) -> OverlapTracker:
        """Crea l'overlap tracker."""
        if self._overlap_tracker is None:
            ov = self.settings.overlap
            self._overlap_tracker = OverlapTracker(
                iou_threshold=ov.iou_threshold,
                position_update_threshold=ov.position_update_threshold,
            )
            logger.info("container.overlap_tracker_created")
        return self._overlap_tracker

    def create_frame_source(self) -> FrameSourcePort:
        """Crea la sorgente frame (WebcamFrameSource da vision-commons)."""
        if self._frame_source is None:
            cam = self.settings.camera
            self._frame_source = WebcamFrameSource(
                resolution=(cam.resolution_width, cam.resolution_height),
            )
            logger.info("container.frame_source_created")
        return self._frame_source

    def create_pipeline(self) -> ObjectMemoryPipeline:
        """Assembla la pipeline completa."""
        if self._pipeline is None:
            self._pipeline = ObjectMemoryPipeline(
                scene_detector=self.create_scene_detector(),
                object_detector=self.create_object_detector(),
                object_labeler=self.create_object_labeler(),
                repository=self.create_repository(),
                snapshot_store=self.create_snapshot_store(),
                overlap_tracker=self.create_overlap_tracker(),
            )
            logger.info("container.pipeline_created")
        return self._pipeline

    def create_query_service(self) -> ObjectQueryService:
        """Crea il query service."""
        if self._query_service is None:
            self._query_service = ObjectQueryService(
                repository=self.create_repository(),
                snapshot_store=self.create_snapshot_store(),
            )
            logger.info("container.query_service_created")
        return self._query_service


__all__ = ["ObjectMemoryContainer"]
