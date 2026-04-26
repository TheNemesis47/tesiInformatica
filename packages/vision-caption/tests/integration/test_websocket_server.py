"""Test di integrazione per il server WebSocket.

Usa httpx con WebSocket support per testare il server FastAPI
senza richiedere GPU o modelli AI (usa mock adapter).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from vision_caption.infrastructure.config.settings import AppSettings
from vision_caption.infrastructure.server.app import create_app


@pytest.fixture
def test_app() -> TestClient:
    """Client di test FastAPI con mock adapter."""
    settings = AppSettings()
    app = create_app(settings=settings, use_mocks=True)
    return TestClient(app)


class TestHealthEndpoint:
    """Test per l'endpoint /health."""

    def test_health_returns_ok(self, test_app: TestClient) -> None:
        """L'endpoint /health risponde con status 'ok'."""
        response = test_app.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert "uptime_sec" in body
        assert "version" in body

    def test_health_has_correct_version(self, test_app: TestClient) -> None:
        """L'endpoint /health restituisce la versione corretta."""
        from vision_caption import __version__
        response = test_app.get("/health")
        assert response.json()["version"] == __version__


class TestWebSocketEndpoint:
    """Test per l'endpoint WebSocket /ws."""

    def test_websocket_connects(self, test_app: TestClient) -> None:
        """La connessione WebSocket può essere stabilita."""
        # TODO: implementare quando il WebSocket handler è completo
        pytest.skip("WebSocket handler non ancora implementato")
