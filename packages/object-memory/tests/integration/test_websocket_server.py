"""Test di integrazione per il server WebSocket di object-memory.

Richiede il server avviato (o usa il client httpx/websockets in-process).
Eseguire con:
    poetry run pytest tests/integration/test_websocket_server.py -v
"""

from __future__ import annotations

import base64
import json

import pytest
from fastapi.testclient import TestClient

from object_memory.infrastructure.server.app import create_app


@pytest.fixture
def test_client() -> TestClient:
    """Client HTTP sincrono per i test di integrazione."""
    app = create_app()
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_ok(self, test_client: TestClient) -> None:
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestObjectsEndpoint:
    def test_list_objects_not_implemented(self, test_client: TestClient) -> None:
        """GET /api/objects è ancora TODO — deve restituire 500 o 501."""
        response = test_client.get("/api/objects")
        # NotImplementedError → FastAPI restituisce 500
        assert response.status_code in (500, 501)

    def test_query_not_implemented(self, test_client: TestClient) -> None:
        """POST /api/query è ancora TODO."""
        payload = {"query": "maglia rossa", "language": "it", "max_results": 3}
        response = test_client.post("/api/query", json=payload)
        assert response.status_code in (500, 501)
