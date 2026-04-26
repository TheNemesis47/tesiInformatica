"""Frame source adapters condivisi."""

from __future__ import annotations

from vision_commons.adapters.frame_source.static_image_source import StaticImageFrameSource
from vision_commons.adapters.frame_source.video_file_source import VideoFileFrameSource
from vision_commons.adapters.frame_source.webcam_source import WebcamFrameSource

__all__ = ["StaticImageFrameSource", "VideoFileFrameSource", "WebcamFrameSource"]
