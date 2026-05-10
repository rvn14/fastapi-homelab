from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import main


def create_test_client(monkeypatch) -> TestClient:
    monkeypatch.setattr(main, "init_db", lambda: None)
    return TestClient(main.app)


def test_root_endpoint(monkeypatch) -> None:
    client = create_test_client(monkeypatch)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FastAPI Homelab Backend is running",
        "version": main.APP_VERSION,
        "docs": "/docs",
        "api": main.API_V1_PREFIX,
    }


def test_health_endpoint(monkeypatch) -> None:
    client = create_test_client(monkeypatch)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
        "service": "FastAPI Homelab Backend",
    }
